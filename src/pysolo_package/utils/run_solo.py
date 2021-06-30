import ctypes
import re
from pysolo_package.utils import radar_structure, DataPair
from pysolo_package.utils.function_alias import aliases
import numpy as np

se_ring_zap = aliases['ring_zap']
isArray = re.compile(r"<class '.*\.LP_c_.*'>")


def array_to_list(input_array, size):
    """ converts ctype array to python list """
    return [input_array[i] for i in range(size)]


def update_boundary_mask(input_list, bad):
    # update boundary mask for new invalid entries that were replaced 
    mask = []
    for i in range(len(input_list)):
        if input_list[i] == np.float32(bad):
            mask.append(True)
        else:
            mask.append(False)
    return mask


def newArray(size, type):
    """ returns an empty float buffer of size """
    data_length_type = type * size
    return ctypes.cast(data_length_type(), ctypes.POINTER(type))


def listToArray(floats, type):
    if floats is None:
        return None
    data_length_type = type * len(floats)
    return ctypes.cast(data_length_type(*floats), ctypes.POINTER(type))


def run_solo_function(c_func, args):

    # Every solo function contains the parameters, "data", "bad", "dgi_clip_gate", and "bad"
    # so here, just extract those values from the args dict.
    input_list_data = args["data"].value
    bad = args["bad"].value
    dgi_clip_gate = args["dgi_clip_gate"].value
    boundary_mask = args["boundary_mask"].value
    
    # none of the solo functions have return types
    c_func.restype = None
    # assuming args is in order according to the signature of the C-function, put the *type* of the args into an ordered list
    c_func.argtypes = [x.type for x in list(args.values())]

    # retrieve size of input/output/mask array
    data_length = len(input_list_data)

    # nGates will always be the size of data_length, so update its value to args dict.
    args["nGates"].value = data_length

    # optional parameters, if None, then set to default values.
    if boundary_mask is None:
        boundary_mask = [True] * data_length # setting boundary mask to all true here will mean C-function does operation on entire dataset. 
    if dgi_clip_gate is None:
        args["dgi_clip_gate"].value = data_length # usually makes sense to make dgi to nGates.
    

    # before running c-functions, all python lists need to be converted to C-type arrays first.

    # create a ctypes array from the input data list, of type 'c_float'
    input_array = listToArray(input_list_data, ctypes.c_float)
    # and replace the list to this array in args
    args["data"].value = input_array

    # se_threshold takes an additional array, thr_data, so create array if needed.
    if "thr_data" in args:
        threshold_list_data = args["thr_data"].value
        threshold_array = listToArray(threshold_list_data, ctypes.c_float)
        args["thr_data"].value = threshold_array

    # boundary list to array, of type 'c_bool'
    boundary_array = listToArray(boundary_mask, ctypes.c_bool)
    args["boundary_mask"].value = boundary_array

    # se_flag functions use bad_flag_masks, so create arrays for those when needed.
    if "bad_flag_mask" in args:
        bad_flags_array = listToArray(args["bad_flag_mask"].value, ctypes.c_bool)
        args["bad_flag_mask"].value = bad_flags_array

    # most functions have "newData", the C-functions take in an empty pointer for
    # "newData", so create a newArray with specified length and type c_float
    if "newData" in args:
        output_array = newArray(data_length, ctypes.c_float)
        args["newData"].value = output_array

    # last_good_v0 only used in unfold_first_good_gate
    if "last_good_v0" in args:
        last_good_array = listToArray(args["last_good_v0"].value, ctypes.c_float)
        args["last_good_v0"].value = last_good_array

    # create a list of values to represent the input parameters to call the C-functions
    # this assumes args is already in order of signature.
    parameters = [x.value if isArray.search(str(x.type)) else x.type(x.value) for x in args.values()]

    # run the actual function here. 
    c_func(*parameters)

    # running c_func either:
    # updated "newData" with... new data
    # or
    # updated "bad_flag_mask" with new masks

    if "newData" in args: # if newData was updated...
        # convert resultant ctypes array back to python list
        output_list = array_to_list(output_array, data_length)
        # update the boundary 
        output_list_mask = update_boundary_mask(output_list, bad)
        return radar_structure.RayData(output_list, output_list_mask)
    elif "bad_flag_mask" in args:
        output_flag_list = array_to_list(bad_flags_array, data_length)
        return radar_structure.RayData(input_list_data, output_flag_list)

    raise Exception("Unexpected control flow.")


def main():

    input_list_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
    bad = -3
    from_km = 2
    to_km = 9
    dgi_clip_gate = 10
    boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]

    input_list_mask = None

    args = {
        "from_km" : DataPair.DataTypeValue(ctypes.c_size_t, from_km),
        "to_km" : DataPair.DataTypeValue(ctypes.c_size_t, to_km),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    output_data = run_solo_function(se_ring_zap, args)
    expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
    assert (output_data.data == expected_data), "PROBLEM"
    return


if __name__ == "__main__":
    main()    
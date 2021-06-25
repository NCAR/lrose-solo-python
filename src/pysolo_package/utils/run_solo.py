import ctypes
import re
import sys
from pathlib import Path
# directory = Path.cwd() / Path('src/')
# sys.path.append(str(directory))
from pysolo_package.utils import radar_structure, ctypes_helper, masked_op
from pysolo_package.utils.function_alias import aliases

se_ring_zap = aliases['ring_zap']
isArray = re.compile(r"<class '.*\.LP_c_.*'>")


def run_solo_function(c_func, args, input_list_mask):

    input_list_data = args["data"].value
    bad = args["bad"].value
    dgi_clip_gate = args["dgi_clip_gate"].value
    boundary_mask = args["boundary_mask"].value

    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))
    
    c_func.restype = None
    c_func.argtypes = [x.type for x in list(args.values())]

    # retrieve size of input/output/mask array
    data_length = len(input_list_data)
    args["nGates"].value = data_length

    # optional parameters
    if boundary_mask is None:
        boundary_mask = [True] * data_length
    if dgi_clip_gate is None:
        args["dgi_clip_gate"].value = data_length
    if input_list_mask is None:
        input_list_mask = [True if x == bad else False for x in input_list_data]   

    # create a ctypes float/bool array from a list of size data_length
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)
    args["data"].value = input_array

    if "thr_data" in args:
        threshold_list_data = args["thr_data"].value
        threshold_array = ctypes_helper.initialize_float_array(data_length, threshold_list_data)
        args["thr_data"].value = threshold_array

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)
    args["boundary_mask"].value = boundary_array

    if "bad_flag_mask" in args:
        bad_flags_array = ctypes_helper.initialize_bool_array(data_length, input_list_mask)
        args["bad_flag_mask"].value = bad_flags_array

    # initialize an empty float array of length
    if "newData" in args:
        output_array = ctypes_helper.initialize_float_array(data_length)
        args["newData"].value = output_array

    if "last_good_v0" in args:
        last_good_array = ctypes_helper.initialize_float_array(len(args["last_good_v0"].value), args["last_good_v0"].value)
        args["last_good_v0"].value = last_good_array

    # parameters = [x.type(x.value) for x in list(args.values())]

    # parameters = []
    # for i, packaged in enumerate(list(args.values())):
    #     if (isArray.search(str(packaged.type))):
    #         parameters.append(packaged.value)
    #     else:
    #         parameters.append(packaged.type(packaged.value))

    parameters = [x.value if isArray.search(str(x.type)) else x.type(x.value) for x in args.values()]

    # print(*parameters)
    c_func(*parameters)

    if "newData" in args:
        # convert resultant ctypes array back to python list
        output_list = ctypes_helper.array_to_list(output_array, data_length)
        output_list_mask, changes = ctypes_helper.update_boundary_mask(output_list, bad, input_list_mask)
        return radar_structure.RayData(output_list, output_list_mask, changes)
    elif "bad_flag_mask" in args:
        output_flag_list = ctypes_helper.array_to_list(bad_flags_array, data_length)
        return radar_structure.RayData(input_list_data, output_flag_list, 0)

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
        "from_km" : ctypes_helper.DataTypeValue(ctypes.c_size_t, from_km),
        "to_km" : ctypes_helper.DataTypeValue(ctypes.c_size_t, to_km),
        "data" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : ctypes_helper.DataTypeValue(ctypes.c_size_t, None),
        "bad" : ctypes_helper.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : ctypes_helper.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    output_data = run_solo_function(se_ring_zap, args, input_list_mask)
    expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
    assert (output_data.data == expected_data), "PROBLEM"


    return


if __name__ == "__main__":
    main()
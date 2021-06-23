import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper, masked_op
from pysolo_package.utils.function_alias import aliases
from pysolo_package.utils.enums import Where

se_threshold = aliases['threshold']

def threshold(input_list_data, thr_list, bad, where, scaled_thr1, scaled_thr2, input_list_mask=None, dgi_clip_gate=None, thr_missing=None, first_good_gate=0, boundary_mask=None):
    """
        Performs a <todo>

        Args:
            input_list: A list containing float data.
            thr_list: The referenced list for threshold
            bad: A float that represents a missing/invalid data point for input_list.
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2)
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold
            (optional) input_list_mask: A list of bools for masking valid/invalid values for input_list (default: a list with True entries for all 'bad' values in 'input_list_data'),
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) thr_missing: A float that represents a missing/invalid data point for thr_list (default: same value as bad)
            (optional) first_good_gate: Marks the index of the first "good" value in the input_list (default: 0) 
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    if (len(input_list_data) != len(thr_list)):
        raise ValueError(("data size (%d) and threshold size (%d) must be of equal size.") % (len(input_list_data), len(thr_list)))
    elif (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))

    # set return type and arg types
    se_threshold.restype = None
    se_threshold.argtypes = [
        ctypes.c_int,                           # where
        ctypes.c_float,                         # scaled_thr1
        ctypes.c_float,                         # scaled_thr2
        ctypes.c_int,                           # first_good_gate
        ctypes.POINTER(ctypes.c_float),         # data
        ctypes.POINTER(ctypes.c_float),         # thr_data
        ctypes.c_size_t,                        # nGates
        ctypes.POINTER(ctypes.c_float),         # newData
        ctypes.c_float,                         # bad
        ctypes.c_float,                         # thr_missing
        ctypes.c_size_t,                        # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool),          # boundary_mask
        ctypes.POINTER(ctypes.c_bool)           # bad_flag_mask
        ]


    # retrieve size of input/output/mask array
    data_length = len(input_list_data)

    # optional parameters
    if boundary_mask == None:
        boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length
    if thr_missing == None:
        thr_missing = bad
    if input_list_mask == None:
        input_list_mask = [True if x == bad else False for x in input_list_data]        
        
    # create a ctypes float/bool array from a list of size data_length
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)
    
    threshold_array = ctypes_helper.initialize_float_array(data_length, thr_list)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)



    # run C function, output_array is updated with despeckle results
    se_threshold(
        ctypes.c_int(where),
        ctypes.c_float(scaled_thr1),
        ctypes.c_float(scaled_thr2),
        ctypes.c_int(first_good_gate),
        input_array,
        threshold_array,
        ctypes.c_size_t(data_length),
        output_array,
        ctypes.c_float(bad),
        ctypes.c_float(thr_missing),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array,
        boundary_array
    )

    # convert resultant ctypes array back to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    output_list_mask, changes = ctypes_helper.update_boundary_mask(output_list, bad, input_list_mask)

    # returns the new data and masks packaged in an object
    return radar_structure.RayData(output_list, output_list_mask, changes)


def threshold_masked(masked_array, threshold_array, where, scaled_thr1, scaled_thr2, boundary_mask=None):
    """ 
        Performs a threshold mask operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            threshold_array: A numpy masked array data structure for referenced threshold,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2)
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold
            
        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(threshold, masked_array, where, scaled_thr1, scaled_thr2, boundary_mask = boundary_mask, second_masked_array=threshold_array)

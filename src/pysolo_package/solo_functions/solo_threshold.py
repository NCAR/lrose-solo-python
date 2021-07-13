import ctypes

from pysolo_package.utils.run_solo import run_solo_function
from pysolo_package.utils import DataPair, masked_op
from pysolo_package.utils.function_alias import aliases
from pysolo_package.utils.enums import Where

se_threshold = aliases['threshold_field']

def threshold(input_list_data, threshold_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, thr_missing=None, first_good_gate=0, boundary_mask=None):
    """
        Performs a <todo>

        Args:
            input_list: A list containing float data.
            thr_list: The referenced list for threshold
            bad: A float that represents a missing/invalid data point for input_list.
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2)
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) thr_missing: A float that represents a missing/invalid data point for thr_list (default: same value as bad)
            (optional) first_good_gate: Marks the index of the first "good" value in the input_list (default: 0) 
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    args = {
        "where" : DataPair.DataTypeValue(ctypes.c_int, where),
        "scaled_thr1" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr1),
        "scaled_thr2" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr2),
        "first_good_gate" : DataPair.DataTypeValue(ctypes.c_int, first_good_gate),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "thr_data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), threshold_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "thr_bad" : DataPair.DataTypeValue(ctypes.c_float, thr_missing if thr_missing else bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask)
    }

    return run_solo_function(se_threshold, args)


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

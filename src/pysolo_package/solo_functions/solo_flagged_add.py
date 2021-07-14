import ctypes

from pysolo_package.utils.enums import Where
from pysolo_package.utils.run_solo import run_solo_function
from pysolo_package.utils import DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_flagged_add = aliases['flagged_add']

def flagged_add(input_list_data, bad, f_const, multiply, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a TODO on a list of data.
        
        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
                      if from_km is greater than to_km,
                      if from_km is less than 0 or if to_km is greater than length of input list.
    """

    args = {
        "f_const" : DataPair.DataTypeValue(ctypes.c_float, f_const),
        "multiply" : DataPair.DataTypeValue(ctypes.c_bool, multiply),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "flag" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask),
    }

    return run_solo_function(se_flagged_add, args)


def flagged_add_masked(masked_array, f_const, multiply, boundary_mask=None):
    """ 
        Performs a <TODO> operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    return masked_op.masked_func(flagged_add, masked_array, f_const, multiply, boundary_mask = boundary_mask, usesBadFlags=True)

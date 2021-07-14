import ctypes

from pysolo_package.utils.enums import Where
from pysolo_package.utils.run_solo import run_solo_function
from pysolo_package.utils import DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_copy_bad_flags = aliases['copy_bad_flags']

def copy_bad_flags(input_list_data, bad, dgi_clip_gate=None, boundary_mask=None):
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
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), [False]*len(input_list_data)),
    }

    return run_solo_function(se_copy_bad_flags, args)


def copy_bad_flags_masked(masked_array, boundary_mask=None):
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
    return masked_op.masked_func(copy_bad_flags, masked_array, boundary_mask = boundary_mask, usesBadFlags=True)

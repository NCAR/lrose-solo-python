import ctypes
import numpy as np

from . import run_solo_function
from . import DataPair, masked_op
from . import aliases

se_assert_bad_flags = aliases['assert_bad_flags']

def assert_bad_flags(input_list_data, bad, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Forces gates to become "bad" value if mask is set to True for that entry, otherwise remains the same
        
        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            bad_flag_mask: A mask for input_list marking good or bad values.
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,

    """

    args = {
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask),
    }

    return run_solo_function(se_assert_bad_flags, args)


def assert_bad_flags_masked(masked_array, boundary_masks=None):
    """ 
        Forces gates to become "bad" value if mask is set to True for that entry, otherwise remains the same
        
        Args:
            masked_array: A numpy masked array data structure,

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    return masked_op.masked_func(assert_bad_flags, masked_array, boundary_masks = boundary_masks, usesBadFlags=True)

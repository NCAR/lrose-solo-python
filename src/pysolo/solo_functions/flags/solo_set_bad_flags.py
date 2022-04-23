import ctypes

from . import Where
from . import run_solo_function
from . import DataPair, masked_op
from . import aliases

se_set_bad_flags = aliases['set_bad_flags']

def set_bad_flags(input_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Masks values in Where region set by 'where' and 'scaled_thr1/2', otherwise, mask is unchanged.
        
        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2) [Note: Not inclusive]
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,

    """

    if isinstance(where, Where):
        where = where.value

    if not isinstance(where, int):
        raise ValueError(f"Expected integer or Where enum for 'where' parameter, received {type(where)}")

    args = {
        "where" : DataPair.DataTypeValue(ctypes.c_int, where),
        "scaled_thr1" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr1),
        "scaled_thr2" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr2),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), [False] * len(input_list_data)),
    }

    return run_solo_function(se_set_bad_flags, args)


def set_bad_flags_masked(masked_array, where, scaled_thr1, scaled_thr2, boundary_mask=None):
    """ 
        Masks values in Where region set by 'where' and 'scaled_thr1/2', otherwise, mask is unchanged.
        
        Args:
            masked_array: A numpy masked array data structure,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2) [Note: Not inclusive]
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    return masked_op.masked_func(set_bad_flags, masked_array, where, scaled_thr1, scaled_thr2, boundary_masks = boundary_masks, usesBadFlags=True)

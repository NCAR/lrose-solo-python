import ctypes

from . import Where
from . import run_solo_function
from . import DataPair, masked_op
from . import aliases

se_bad_flags_logic = aliases['bad_flags_logic']

def bad_flags_logic(input_list_data, bad, where, logical, scaled_thr1, scaled_thr2, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a logical operation (LOGICAL enum) between bad_flag_mask and a value based on the WHERE enum.
        Equivalent to:
        flags[i] = (value[i] > WHERE) {logical operand} (bad_flag_mask[i]):

        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2) [Note: Not inclusive]
            logical: A 'Logical' enum, AND(0), OR(1), XOR(2)
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
        "scaled_thr1" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr1),
        "scaled_thr2" : DataPair.DataTypeValue(ctypes.c_float, scaled_thr2),
        "where" : DataPair.DataTypeValue(ctypes.c_int, where),
        "logical" : DataPair.DataTypeValue(ctypes.c_int, logical),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "flag" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask),
    }

    return run_solo_function(se_bad_flags_logic, args)


def bad_flags_logic_masked(masked_array, where, logical, scaled_thr1, scaled_thr2, boundary_mask=None):
    """ 
        Performs a logical operation (LOGICAL enum) between bad_flag_mask and a value based on the WHERE enum.
        
        Args:
            masked_array: A numpy masked array data structure,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2) [Note: Not inclusive]
            logical: A 'Logical' enum, AND(0), OR(1), XOR(2)
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    return masked_op.masked_func(bad_flags_logic, masked_array, where, logical, scaled_thr1, scaled_thr2, boundary_masks = boundary_masks, usesBadFlags=True)

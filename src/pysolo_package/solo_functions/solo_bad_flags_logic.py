import ctypes

from pysolo_package.utils.enums import Where
from pysolo_package.utils.run_solo import run_solo_function
from pysolo_package.utils import DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_bad_flags_logic = aliases['bad_flags_logic']

def bad_flags_logic(input_list_data, bad,  where, logical, scaled_thr1, scaled_thr2, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a TODO on a list of data.
        
        Args:
            input_list_data_1: <TODO>,
            bad: A float that represents a missing/invalid data point,
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2) [Note: Not inclusive]
            logical: A 'Logical' enum, AND(0), OR(1), XOR(2)
            scaled_thr1: Lower bound threshold
            scaled_thr2: Upper bound threshold
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
                      if from_km is greater than to_km,
                      if from_km is less than 0 or if to_km is greater than length of input list.
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
    return masked_op.masked_func(bad_flags_logic, masked_array, where, logical, scaled_thr1, scaled_thr2, boundary_mask = boundary_mask, usesBadFlags=True)
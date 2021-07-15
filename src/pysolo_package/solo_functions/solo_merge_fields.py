import ctypes

from ..utils.run_solo import run_solo_function
from ..utils import DataPair, masked_op
from ..utils.function_alias import aliases

se_merge_fields = aliases['merge_fields']

def merge_fields(input_list_data_1, input_list_data_2, bad, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a TODO on a list of data.
        
        Args:
            input_list_data_1: <TODO>,
            input_list_data_2: <TODO>,
            bad: A float that represents a missing/invalid data point,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
                      if from_km is greater than to_km,
                      if from_km is less than 0 or if to_km is greater than length of input list.
    """

    args = {
        "data1" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data_1),
        "data2" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data_2),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_merge_fields, args)


def merge_fields_masked(masked_array, boundary_mask=None):
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
    return masked_op.masked_func(merge_fields, masked_array,  boundary_mask = boundary_mask)

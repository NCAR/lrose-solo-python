import ctypes
import pyart
import numpy as np
from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases


se_despeckle = aliases['despeckle']


def despeckle(input_list_data, bad, a_speckle, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a despeckle operation on a list of data (a single ray)

        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            a_speckle: An integer that determines the number of contiguous good data considered a speckle,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list),
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            Numpy masked array: Contains an array of data, mask, and fill_value of results.

    """

    args = {
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "a_speckle" : DataPair.DataTypeValue(ctypes.c_size_t, a_speckle),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_despeckle, args)


def despeckle_masked(masked_array, a_speckle, boundary_masks=None):
   return masked_op.masked_func_v2(despeckle, masked_array, {'boundary_mask': boundary_masks}, {'a_speckle': a_speckle})


def despeckle_field(radar: pyart.core.Radar, field: str, new_field: str, a_speckle: int, boundary_masks=None, sweep=0):
    field_masked_array = radar.fields[field]['data']
    despeckled_mask = despeckle_masked(field_masked_array, a_speckle, boundary_masks)
    radar.add_field_like(field, new_field, despeckled_mask, replace_existing=True)

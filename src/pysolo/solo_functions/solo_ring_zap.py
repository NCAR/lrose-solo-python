import ctypes
import numpy as np
from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_ring_zap = aliases['ring_zap']

def ring_zap(input_list_data, bad, from_km, to_km, km_between_gates=1, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a ring zap operation on a list of data.
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            from_km: An integer for the starting range,
            to_km: An integer for the ending range,
            (optional) km_between_gates: An integer representing the distance (in km) between gates (default: 1 km).
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list).
            (optional) boundary_mask: Defines region over which operations will be done (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

    """

    from_km = int(from_km / km_between_gates)
    to_km = int(to_km / km_between_gates)

    args = {
        "from_km" : DataPair.DataTypeValue(ctypes.c_size_t, from_km),
        "to_km" : DataPair.DataTypeValue(ctypes.c_size_t, to_km),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_ring_zap, args)


def ring_zap_masked(masked_array, from_km, to_km, km_between_gates, boundary_masks=None):
    """ 
        Performs a ring zap operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            from_km: An integer for the starting range,
            to_km: An integer for the ending range,
            km_between_gates: An integer representing the distance (in km) between gates

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    from_km = int(from_km / km_between_gates)
    to_km = int(to_km / km_between_gates)
    return masked_op.masked_func_v2(ring_zap, masked_array, {'boundary_mask': boundary_masks}, {'from_km': from_km, 'to_km': to_km})

    return masked_op.masked_func(ring_zap, masked_array, from_km, to_km, boundary_masks = boundary_masks)

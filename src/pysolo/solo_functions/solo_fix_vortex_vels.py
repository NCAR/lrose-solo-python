import ctypes
import numpy as np
from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_fix_vortex_vels = aliases['fix_vortex_vels']

def fix_vortex_vels_ray(input_list_data, bad, vs_data, vl_data, vs_xmitted_freq, vs_interpulse_time, vl_interpulse_time, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a TODO on a list of data.

        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            vs_data: <TODO>
            vl_data: <TODO>
            vs_xmitted_freq: <TODO>
            vs_interpulse_time: <TODO>
            vl_interpulse_time: <TODO>
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
        "vs_data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), vs_data),
        "vl_data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), vl_data),
        "vs_xmitted_freq" : DataPair.DataTypeValue(ctypes.c_float, vs_xmitted_freq),
        "vs_interpulse_time" : DataPair.DataTypeValue(ctypes.c_float, vs_interpulse_time),
        "vl_interpulse_time" : DataPair.DataTypeValue(ctypes.c_float, vl_interpulse_time),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_fix_vortex_vels, args)


def fix_vortex_vels_masked(masked_array, vs_data, vl_data, vs_xmitted_freq, vs_interpulse_time, vl_interpulse_time, boundary_masks=None):
    """
        Performs a ring zap operation on a numpy masked array

        Args:
            masked_array: A numpy masked array data structure,
            vs_data: <TODO>
            vl_data: <TODO>
            vs_xmitted_freq: <TODO>
            vs_interpulse_time: <TODO>
            vl_interpulse_time: <TODO>
            km_between_gates: An integer representing the distance (in km) between gates

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(fix_vortex_vels_ray, masked_array, vs_data, vl_data, vs_xmitted_freq, vs_interpulse_time, vl_interpulse_time, boundary_masks = boundary_masks)

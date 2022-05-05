import ctypes

import numpy as np

from ..c_wrapper.run_solo import run_solo_function

from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_remove_ac_motion = aliases['remove_ac_motion']



def remove_ac_motion_ray(input_list_data, bad, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, seds_nyquist_velocity, dgi_clip_gate=None,
        boundary_mask=None):
    """
        Performs a <TODO> operation on a list of data.

        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            vert_velocity: <TODO>
            ew_velocity: <TODO>
            ns_velocity: <TODO>
            ew_gndspd_corr: <TODO>
            tilt: <TODO>
            elevation: <TODO>
            dds_radd_eff_unamb_vel: <TODO>
            seds_nyquist_velocity: <TODO>
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "vert_velocity" : DataPair.DataTypeValue(ctypes.c_float, vert_velocity),
        "ew_velocity" : DataPair.DataTypeValue(ctypes.c_float, ew_velocity),
        "ns_velocity" : DataPair.DataTypeValue(ctypes.c_float, ns_velocity),
        "ew_gndspd_corr" : DataPair.DataTypeValue(ctypes.c_float, ew_gndspd_corr),
        "tilt" : DataPair.DataTypeValue(ctypes.c_float, tilt),
        "elevation" : DataPair.DataTypeValue(ctypes.c_float, elevation),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "dds_radd_eff_unamb_vel" : DataPair.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "seds_nyquist_velocity" : DataPair.DataTypeValue(ctypes.c_float, seds_nyquist_velocity),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_remove_ac_motion, args)


def remove_ac_motion_masked(masked_array, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, seds_nyquist_velocity, boundary_masks=None):
    """
        Performs a <TODO> operation on a numpy masked array

        Args:
            masked_array: A numpy masked array data structure,
            vert_velocity: <TODO>
            ew_velocity: <TODO>
            ns_velocity: <TODO>
            ew_gndspd_corr: <TODO>
            tilt: <TODO>
            elevation: <TODO>
            dds_radd_eff_unamb_vel: <TODO>
            seds_nyquist_velocity: <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """


    return masked_op.masked_func(remove_ac_motion_ray, masked_array, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, seds_nyquist_velocity,
        boundary_masks = boundary_masks)

import ctypes
from pysolo_package.utils.run_solo import run_solo_function

from pysolo_package.utils import radar_structure, DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_unfold_local_wind = aliases['BB_unfold_local_wind']

def unfold_local_wind(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind,  ns_wind,  ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a <TODO>

        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            nyquist_velocity: <TODO>,
            dds_radd_eff_unamb_vel: <TODO>,
            azimuth_angle_degrees: <TODO>,
            elevation_angle_degrees: <TODO>,
            ew_wind: <TODO>,
            ns_wind: <TODO>,
            ud_wind: <TODO>,
            max_pos_folds: <TODO>,
            max_neg_folds: <TODO>,
            ngates_averaged: <TODO>,
            last_good_v0: <TODO>,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "nyquist_velocity" : DataPair.DataTypeValue(ctypes.c_float, nyquist_velocity),
        "dds_radd_eff_unamb_vel" : DataPair.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "azimuth_angle_degrees" : DataPair.DataTypeValue(ctypes.c_float, azimuth_angle_degrees),
        "elevation_angle_degrees" : DataPair.DataTypeValue(ctypes.c_float, elevation_angle_degrees),
        "ew_wind" : DataPair.DataTypeValue(ctypes.c_float, ew_wind),
        "ns_wind" : DataPair.DataTypeValue(ctypes.c_float, ns_wind),
        "ud_wind" : DataPair.DataTypeValue(ctypes.c_float, ud_wind),
        "max_pos_folds" : DataPair.DataTypeValue(ctypes.c_int, max_pos_folds),
        "max_neg_folds" : DataPair.DataTypeValue(ctypes.c_int, max_neg_folds),
        "ngates_averaged" : DataPair.DataTypeValue(ctypes.c_size_t, ngates_averaged),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_unfold_local_wind, args)


def unfold_local_wind_masked(masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, boundary_mask=None):
    """
        Performs a <TODO> on a numpy masked array

        Args:
            masked_array: A numpy masked array data structure,
            nyquist_velocity: <TODO>
            dds_radd_eff_unamb_vel: <TODO>
            max_pos_folds: <TODO>
            max_neg_folds: <TODO>
            ngates_averaged: <TODO>
            last_good_v0: <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    
    return masked_op.masked_func(unfold_local_wind, masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, boundary_mask = boundary_mask)

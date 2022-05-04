import ctypes
import pyart
import numpy as np

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_unfold_local_wind = aliases['BB_unfold_local_wind']


def unfold_local_wind_ray(
        input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged,
        dgi_clip_gate=None, boundary_mask=None):
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
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "data": DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates": DataPair.DataTypeValue(ctypes.c_size_t, None),
        "nyquist_velocity": DataPair.DataTypeValue(ctypes.c_float, nyquist_velocity),
        "dds_radd_eff_unamb_vel": DataPair.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "azimuth_angle_degrees": DataPair.DataTypeValue(ctypes.c_float, azimuth_angle_degrees),
        "elevation_angle_degrees": DataPair.DataTypeValue(ctypes.c_float, elevation_angle_degrees),
        "ew_wind": DataPair.DataTypeValue(ctypes.c_float, ew_wind),
        "ns_wind": DataPair.DataTypeValue(ctypes.c_float, ns_wind),
        "ud_wind": DataPair.DataTypeValue(ctypes.c_float, ud_wind),
        "max_pos_folds": DataPair.DataTypeValue(ctypes.c_int, max_pos_folds),
        "max_neg_folds": DataPair.DataTypeValue(ctypes.c_int, max_neg_folds),
        "ngates_averaged": DataPair.DataTypeValue(ctypes.c_size_t, ngates_averaged),
        "bad": DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate": DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask": DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_unfold_local_wind, args)


def unfold_local_wind_masked(
        masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged,
        boundary_masks=None):
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

    return masked_op.masked_func_iterable(
        unfold_local_wind_ray,
        masked_array,
        {
            'boundary_mask': boundary_masks,
            'azimuth_angle_degrees': azimuth_angle_degrees,
            'elevation_angle_degrees': elevation_angle_degrees
        },
        {
            'nyquist_velocity': nyquist_velocity,
            'dds_radd_eff_unamb_vel': dds_radd_eff_unamb_vel,
            'ew_wind': ew_wind,
            'ns_wind': ns_wind,
            'ud_wind': ud_wind,
            'max_pos_folds': max_pos_folds,
            'max_neg_folds': max_neg_folds,
            'ngates_averaged': ngates_averaged
        }
    )


def unfold_local_wind_fields(radar: pyart.core.Radar, field: str, new_field: str, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, boundary_masks=None, sweep=0):

    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        print(sm)
        nyquist_velocity = sm.radar.get_nyquist_vel(sm.sweep)
        dds_radd_eff_unamb_vel = nyquist_velocity
        azimuth_angle_degrees = list(sm.radar.get_azimuth(sm.sweep))
        elevation_angle_degrees = list(sm.radar.get_elevation(sm.sweep))

        sm.new_masked_array = unfold_local_wind_masked(sm.radar_sweep_data, nyquist_velocity, dds_radd_eff_unamb_vel,
                                                    azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, boundary_masks)

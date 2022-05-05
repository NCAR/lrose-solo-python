import ctypes
import pyart
import numpy as np

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import  DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_funfold = aliases['funfold']

def forced_unfolding_ray(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, center, dgi_clip_gate=None, boundary_mask=None):
    """
       Forces all data points to fall within plus or minus the Nyquist

        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            nyquist_velocity: Float value obtained from the radar,
            dds_radd_eff_unamb_vel: Float value obtained from the radar,
            center: <TODO>,
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
        "nyquist_velocity" : DataPair.DataTypeValue(ctypes.c_float, nyquist_velocity),
        "dds_radd_eff_unamb_vel" : DataPair.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "center" : DataPair.DataTypeValue(ctypes.c_float, center),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_funfold, args)


def forced_unfolding_masked(masked_array, nyquist_velocity: float, dds_radd_eff_unamb_vel: float, center: float, boundary_masks=None):
    """
       Forces all data points to fall within plus or minus the Nyquist

        Args:
            masked_array: A numpy masked array data structure,
            nyquist_velocity: Float value obtained from the radar,
            dds_radd_eff_unamb_vel: Float value obtained from the radar,
            center: <TODO>,

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(forced_unfolding_ray, masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, center, boundary_masks = boundary_masks)


def forced_unfolding_field(radar: pyart.core.Radar, field: str, new_field: str, dds_radd_eff_unamb_vel: float, center: float, boundary_masks=None, sweep=0):

    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        nyquist_velocity = sm.radar.get_nyquist_vel(sweep)
        sm.new_masked_array = forced_unfolding_masked(sm.radar_sweep_data, nyquist_velocity, dds_radd_eff_unamb_vel, center, boundary_masks)

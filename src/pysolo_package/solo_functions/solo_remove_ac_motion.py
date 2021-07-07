import ctypes

from pysolo_package.utils.run_solo import run_solo_function

from pysolo_package.utils import DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_remove_ac_motion = aliases['remove_ac_motion']

# extern "C" SOLO_API void se_remove_ac_motion(float vert_velocity, float ew_velocity, float ns_velocity,
# float ew_gndspd_corr, float tilt, float elevation,
# const float* data, float* newData, size_t nGates,
# float bad, size_t dgi_clip_gate,
# float dds_radd_eff_unamb_vel,
# float seds_nyquist_velocity, bool* bnd);


def remove_ac_motion(input_list_data, bad, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, seds_nyquist_velocity, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a <TODO> operation on a list of data.
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            seds_gate_diff_interval: <TODO>
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

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
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "dds_radd_eff_unamb_vel" : DataPair.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "seds_nyquist_velocity" : DataPair.DataTypeValue(ctypes.c_float, seds_nyquist_velocity),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_remove_ac_motion, args)


def remove_ac_motion_masked(masked_array, seds_gate_diff_interval, boundary_mask=None):
    """ 
        Performs a <TODO> operation on a numpy masked array
        
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


    return masked_op.masked_func(remove_ac_motion, masked_array, seds_gate_diff_interval, boundary_mask = boundary_mask)
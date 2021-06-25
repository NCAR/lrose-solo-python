import ctypes
from pysolo_package.utils.run_solo import run_solo_function

from pysolo_package.utils import radar_structure, ctypes_helper, masked_op
from pysolo_package.utils.function_alias import aliases

se_funfold = aliases['forced_unfolding']

def forced_unfolding(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, center, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a <TODO>
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            nyquist_velocity: <TODO>, 
            dds_radd_eff_unamb_vel: <TODO>, 
            center: <TODO>,
            (optional) input_list_mask: A list of bools for masking valid/invalid values for input_list (default: a list with True entries for all 'bad' values in 'input_list_data'),
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
                      if from_km is greater than to_km,
                      if from_km is less than 0 or if to_km is greater than length of input list.
    """

    args = {
        "data" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : ctypes_helper.DataTypeValue(ctypes.c_size_t, None),
        "nyquist_velocity" : ctypes_helper.DataTypeValue(ctypes.c_float, nyquist_velocity),
        "dds_radd_eff_unamb_vel" : ctypes_helper.DataTypeValue(ctypes.c_float, dds_radd_eff_unamb_vel),
        "center" : ctypes_helper.DataTypeValue(ctypes.c_float, center),
        "bad" : ctypes_helper.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : ctypes_helper.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_funfold, args, input_list_mask)


def forced_unfolding_masked(masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, center, boundary_mask=None):
    """ 
        Performs a ring zap operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            nyquist_velocity: <TODO>, 
            dds_radd_eff_unamb_vel: <TODO>, 
            center: <TODO>,

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(forced_unfolding, masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, center, boundary_mask = boundary_mask)

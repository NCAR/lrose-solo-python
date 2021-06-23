import ctypes

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

    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))

    # set return type and arg types
    se_funfold.restype = None
    se_funfold.argtypes = [
        ctypes.POINTER(ctypes.c_float), 
        ctypes.POINTER(ctypes.c_float), 
        ctypes.c_size_t, 
        ctypes.c_float, 
        ctypes.c_float, 
        ctypes.c_float, 
        ctypes.c_float, 
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_bool)
        ]


    # retrieve size of input/output/mask array
    data_length = len(input_list_data)

    # optional parameters
    if boundary_mask == None:
        boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length
    if input_list_mask == None:
        input_list_mask = [True if x == bad else False for x in input_list_data]    
        
    # create a ctypes float/bool array from a list of size data_length
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)


    # run C function, output_array is updated with despeckle results
    se_funfold(
        input_array, 
        output_array, 
        ctypes.c_size_t(data_length), 
        ctypes.c_float(nyquist_velocity), 
        ctypes.c_float(dds_radd_eff_unamb_vel), 
        ctypes.c_float(center), 
        ctypes.c_float(bad), 
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array
    )

    # convert resultant ctypes array back to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    output_list_mask, changes = ctypes_helper.update_boundary_mask(output_list, bad, input_list_mask)

    # returns the new data and masks packaged in an object
    return radar_structure.RayData(output_list, output_list_mask, changes)


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

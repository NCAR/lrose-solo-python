import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_ring_zap = aliases['ring_zap']

def ring_zap(from_km, to_km, input_list, bad, input_boundary_mask, dgi_clip_gate=None, boundary_mask_all_true=False):
    """ 
        Performs a ring zap operation on a list of data.
        
        Args:
            from_km: An integer for the starting range,
            to_km: An integer for the ending range,
            input_list: A list containing float data,
            bad_value: A float that represents a missing/invalid data point,
            input_boundary_mask: A list of bools for masking valid/invalid values for input_list,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False).

        Returns:
          RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
                      if from_km is greater than to_km,
                      if from_km is less than 0 or if to_km is greater than length of input list.
    """

    if (len(input_list) != len(input_boundary_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(input_boundary_mask)))
    elif (from_km > to_km):
        raise ValueError(("from_km value (%d) must be smaller than to_km value (%d).") % (from_km, to_km))
    elif (from_km < 0):
        raise ValueError(("from_km value (%d) must be greater than zero.") % from_km)
    elif (to_km > len(input_list)):
        raise ValueError(("to_km value (%d) must be less than than the length of the input list (%d).") % (to_km, len(input_list)))

    # set return type and arg types
    se_ring_zap.restype = None
    se_ring_zap.argtypes = [
        ctypes.c_size_t,
        ctypes.c_size_t, 
        ctypes.POINTER(ctypes.c_float), 
        ctypes.POINTER(ctypes.c_float), 
        ctypes.c_size_t, 
        ctypes.c_float, 
        ctypes.c_size_t, 
        ctypes.POINTER(ctypes.c_bool)
        ]

    boundary_mask_output = deepcopy(input_boundary_mask)

    # retrieve size of input/output/mask array
    data_length = len(input_list)

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        input_boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length        
        
    # create a ctypes type that is an array of floats of length from above
    input_array = ctypes_helper.initialize_float_array(data_length, input_list)

    mask_array = ctypes_helper.initialize_bool_array(data_length, input_boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)


    # run C function, output_array is updated with despeckle results
    se_ring_zap(
        ctypes.c_size_t(from_km), 
        ctypes.c_size_t(to_km), 
        input_array, 
        output_array, 
        ctypes.c_size_t(data_length), 
        ctypes.c_float(bad), 
        ctypes.c_size_t(dgi_clip_gate),
        mask_array
    )

    # convert ctypes array to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    boundary_mask_output, changes = ctypes_helper.update_boundary_mask(input_list, output_list, boundary_mask_output)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(output_list, boundary_mask_output, changes)


def ring_zap_masked(masked_array, from_km, to_km, km_between_gates):
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
    try:
        import numpy as np
        missing = masked_array.fill_value
        mask = masked_array.mask.tolist()
        data_list = masked_array.tolist(missing)
    except ModuleNotFoundError:
        print("You must have Numpy installed.")
    except AttributeError:
        print("Expected a numpy masked array.")
    
    output_data = []
    output_mask = []

    from_km = int(from_km / km_between_gates)
    to_km = int(to_km / km_between_gates)

    for i in range(len(data_list)):
        input_data = data_list[i]
        boundary_mask = mask[i]

        # run ring removal
        ring = ring_zap(from_km, to_km, input_data, missing, boundary_mask, boundary_mask_all_true=True)
        output_data.append(ring.data)
        output_mask.append(ring.mask)

    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

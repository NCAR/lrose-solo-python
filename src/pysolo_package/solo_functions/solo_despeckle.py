import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_despeckle = aliases['despeckle']

def despeckle(input_list, bad, a_speckle, boundary_mask_input, dgi_clip_gate=None, boundary_mask_all_true=False):
    """ 
        Performs a despeckle operation on a list of data (a single ray)
        
        Args:
            input_list: A list containing float data.
            bad_value: A float that represents a missing/invalid data point.
            a_speckle: An integer that determines the number of contiguous good data considered a speckle
            boundary_mask_input: A list of bools for masking valid/invalid values for input_list
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
            RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and boundary_mask_input are not equal in size
    """

    if (len(input_list) != len(boundary_mask_input)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(boundary_mask_input)))

    # set return type and arg types
    se_despeckle.restype = None
    se_despeckle.argtypes = [
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float), 
        ctypes.c_size_t, 
        ctypes.c_float, 
        ctypes.c_int, 
        ctypes.c_size_t, 
        ctypes.POINTER(ctypes.c_bool)
        ]

    boundary_mask_output = deepcopy(boundary_mask_input)

    # retrieve size of input/output/mask array
    data_length = len(input_list)
    # create a ctypes type that is an array of floats of length from above
    data_length_type = ctypes.c_float * data_length
    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)

    # create a ctypes type that is an array of bools of length from above
    boundary_length_type = ctypes.c_bool * data_length

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        boundary_mask_input = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length        

    # run C function, output_array is updated with despeckle results
    se_despeckle(data_length_type(*input_list), output_array, ctypes.c_size_t(data_length), ctypes.c_float(bad), ctypes.c_int(a_speckle), ctypes.c_size_t(dgi_clip_gate), boundary_length_type(*boundary_mask_input))

    # convert ctypes array to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    boundary_mask_output, changes = ctypes_helper.update_boundary_mask(input_list, output_list, boundary_mask_output)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(output_list, boundary_mask_output, changes)


def despeckle_masked(masked_array, a_speckle):
    """ 
        Performs a despeckle operation on a numpy masked array
        
        Args:
            masked_array: A list containing float data.
            a_speckle: An integer that determines the number of contiguous good data considered a speckle

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

    for i in range(len(data_list)):
        input_data = data_list[i]
        boundary_mask = mask[i]

        # run despeckle
        despec = despeckle(input_data, missing, a_speckle, boundary_mask, boundary_mask_all_true=True)
        output_data.append(despec.data)
        output_mask.append(despec.mask)

    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

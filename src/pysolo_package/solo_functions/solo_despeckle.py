import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_despeckle = aliases['despeckle']

def despeckle(input_list_data, bad, a_speckle, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a despeckle operation on a list of data (a single ray)

        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            a_speckle: An integer that determines the number of contiguous good data considered a speckle,
            (optional) input_list_mask: A list of bools for masking valid/invalid values for input_list (default: a list with True entries for all 'bad' values in 'input_list_data'),
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list),
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))

    # set return type and arg types
    se_despeckle.restype = None
    se_despeckle.argtypes = [
        ctypes.POINTER(ctypes.c_float),        # data
        ctypes.POINTER(ctypes.c_float),        # newData
        ctypes.c_size_t,                       # nGates
        ctypes.c_float,                        # bad
        ctypes.c_int,                          # a_speckle
        ctypes.c_size_t,                       # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool)          # boundary_mask
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

    # create a ctypes type that is an array of floats of length from above
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)


    # run C function, output_array is updated with despeckle results
    se_despeckle(
        input_array,
        output_array,
        ctypes.c_size_t(data_length),
        ctypes.c_float(bad),
        ctypes.c_int(a_speckle),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array
    )

    # convert ctypes array to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    boundary_mask_output, changes = ctypes_helper.update_boundary_mask(output_list, bad, input_list_mask)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(output_list, boundary_mask_output, changes)


def despeckle_masked(masked_array, a_speckle, boundary_mask=None):
    """
        Performs a despeckle operation on a numpy masked array

        Args:
            masked_array: A numpy masked array data structure,
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
        input_mask = mask[i]

        # run despeckle
        despec = despeckle(input_data, missing, a_speckle, input_list_mask=input_mask, boundary_mask=boundary_mask)
        output_data.append(despec.data)
        output_mask.append(despec.mask)

    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

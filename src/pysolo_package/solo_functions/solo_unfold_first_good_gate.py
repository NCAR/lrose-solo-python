import ctypes

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_unfold_first_good_gate = aliases['unfold_first_good_gate']

def unfold_first_good_gate(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a <TODO>

        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            nyquist_velocity: <TODO>
            dds_radd_eff_unamb_vel: <TODO>
            max_pos_folds: <TODO>
            max_neg_folds: <TODO>
            ngates_averaged: <TODO>
            last_good_v0: <TODO>
            (optional) input_list_mask: A list of bools for masking valid/invalid values for input_list (default: a list with True entries for all 'bad' values in 'input_list_data'),
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False).

        Returns:
          RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (
            len(input_list_data), len(input_list_mask)))

    # set return type and arg types
    se_unfold_first_good_gate.restype = None
    se_unfold_first_good_gate.argtypes = [
        ctypes.POINTER(ctypes.c_float),     # data
        ctypes.POINTER(ctypes.c_float),     # newData
        ctypes.c_size_t,                    # nGates
        ctypes.c_float,                     # nyquist_velocity
        ctypes.c_float,                     # dds_radd_eff_unamb_vel
        ctypes.c_int,                       # max_pos_folds
        ctypes.c_int,                       # max_neg_folds
        ctypes.c_size_t,                    # ngates_averaged
        ctypes.POINTER(ctypes.c_float),     # last_good_v0
        ctypes.c_float,                     # bad_float_value
        ctypes.c_size_t,                    # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool)       # bnd
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

    last_good_v0_array = ctypes_helper.initialize_float_array(len(last_good_v0), last_good_v0)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)

    # run C function, output_array is updated with despeckle results
    se_unfold_first_good_gate(
        input_array,                            # data
        output_array,                           # newData
        ctypes.c_size_t(data_length),           # nGates
        ctypes.c_float(nyquist_velocity),       # nyquist_velocity
        ctypes.c_float(dds_radd_eff_unamb_vel), # dds_radd_eff_unamb_vel
        ctypes.c_int(max_pos_folds),            # max_pos_folds
        ctypes.c_int(max_neg_folds),            # max_neg_folds
        ctypes.c_size_t(ngates_averaged),       # ngates_averaged
        last_good_v0_array,                     # last_good_v0
        ctypes.c_float(bad),                    # bad_float_value
        ctypes.c_size_t(dgi_clip_gate),         # dgi_clip_gate
        boundary_array                          # bnd
    )

    # convert resultant ctypes array back to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    output_list_mask, changes = ctypes_helper.update_boundary_mask(
        output_list, bad, input_list_mask)

    # returns the new data and masks packaged in an object
    return radar_structure.RayData(output_list, output_list_mask, changes)


# TODO: what to do with last_good_v0
def unfold_first_good_gate_masked(masked_array, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, boundary_mask=None):
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

        # run ring removal
        ring = unfold_first_good_gate(input_data, missing, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, input_list_mask=input_mask, boundary_mask=boundary_mask)
        output_data.append(ring.data)
        output_mask.append(ring.mask)

    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

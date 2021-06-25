import ctypes

import sys
from pathlib import Path

from pysolo_package.utils.run_solo import run_solo_function
# directory = Path.cwd() / Path('src/')
# sys.path.append(str(directory))

from pysolo_package.utils import ctypes_helper, masked_op
from pysolo_package.utils.function_alias import aliases

se_ring_zap = aliases['ring_zap']

def ring_zap(input_list_data, bad, from_km, to_km, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a ring zap operation on a list of data.
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            from_km: An integer for the starting range,
            to_km: An integer for the ending range,
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
        "from_km" : ctypes_helper.DataTypeValue(ctypes.c_size_t, from_km),
        "to_km" : ctypes_helper.DataTypeValue(ctypes.c_size_t, to_km),
        "data" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : ctypes_helper.DataTypeValue(ctypes.c_size_t, None),
        "bad" : ctypes_helper.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : ctypes_helper.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : ctypes_helper.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_ring_zap, args, input_list_mask)


def ring_zap_masked(masked_array, from_km, to_km, km_between_gates, boundary_mask=None):
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

    from_km = int(from_km / km_between_gates)
    to_km = int(to_km / km_between_gates)

    return masked_op.masked_func(ring_zap, masked_array, from_km, to_km, boundary_mask = boundary_mask)

def main():

    input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
    bad = -3
    from_km = 2
    to_km = 9
    dgi = 10
    boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]

    input_list_mask = None

    output_data = ring_zap(input_data, bad, from_km, to_km, dgi_clip_gate=dgi, boundary_mask=boundary_mask)

    expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
    assert (output_data.data == expected_data), "PROBLEM"

    return


if __name__ == "__main__":
    main()
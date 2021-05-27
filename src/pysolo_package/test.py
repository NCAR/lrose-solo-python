import ctypes
import os
import platform
from copy import deepcopy


class RadarData:
    """ This object contains fields 'data' and 'mask' of list types"""
    def __init__(self, data, mask):
        self.data = data
        self.mask = mask


dirname = os.path.dirname(os.path.abspath(__file__))

if (platform.system() == "Windows"):
    libraryName = os.path.join(dirname, 'libs/despeckle.dll')
    os.path.join(dirname, libraryName)
    c_lib = ctypes.CDLL(libraryName)
    despeckle = c_lib.se_despeckle
else:
    libraryName = os.path.join(dirname, 'libs/libSolo_18.04.so')
    os.path.join(dirname, libraryName)
    c_lib = ctypes.CDLL(libraryName)
    despeckle = c_lib._Z12se_despecklePKfPfmfimPb


def array_to_list(input_array, size):
    """ converts ctype array to python list """
    return [input_array[i] for i in range(size)]


def initialize_float_array(size):
    """ returns an empty float buffer of size """
    data_length_type = ctypes.c_float * size
    return ctypes.cast(data_length_type(), ctypes.POINTER(ctypes.c_float))


def sampleAddInt(x, y):
    """ This function is to test the Solo SampleAddInt function from despeckle.cc, this returns the sum of two integers. """
    if not isinstance(x, int):
        raise ctypes.ArgumentError("Expected an integer for 1st parameter, received: %s " % x)
    elif not isinstance(y, int):
        raise ctypes.ArgumentError("Expected an integer for 2nd parameter, received: %s " % y)
    c_lib._Z12SampleAddIntii.argtypes = [ctypes.c_int]
    c_lib._Z12SampleAddIntii.restype = ctypes.c_int
    return c_lib._Z12SampleAddIntii(x, y)


def se_despeckle(input_list, bad, a_speckle, dgi_clip_gate, boundary_mask_input, boundary_mask_all_true=False):
    """ 
        Performs a despeckle operation on a list of data
        
        Args:
          input_list: A list containing float data.
          bad_value: A float that represents a missing/invalid data point.
          a_speckle: An integer that determines the number of contiguous good data considered a speckle
          dgi_clip_gate: An integer determines the end of the ray
          boundary_mask_input: A list of bools for masking valid/invalid values for input_list
          (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
          RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
          ValueError: if input_list and boundary_mask_input are not equal in size
    """

    if (len(input_list) != len(boundary_mask_input)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(boundary_mask_input)))

    # set return type and arg types
    despeckle.restype = None
    despeckle.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.c_float, ctypes.c_int, ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]

    boundary_mask_output = deepcopy(boundary_mask_input)

    # retrieve size of input/output/mask array
    data_length = len(input_list)
    # create a ctypes type that is an array of floats of length from above
    data_length_type = ctypes.c_float * data_length
    # initialize an empty float array of length
    output_array = initialize_float_array(data_length)

    # create a ctypes type that is an array of bools of length from above
    boundary_length_type = ctypes.c_bool * data_length

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        boundary_mask_input = [True] * data_length

    # run C function, output_array is updated with despeckle results
    despeckle(data_length_type(*input_list), output_array, ctypes.c_size_t(data_length), ctypes.c_float(bad), ctypes.c_int(a_speckle), ctypes.c_size_t(dgi_clip_gate), boundary_length_type(*boundary_mask_input))

    # convert ctypes array to python list
    output_list = array_to_list(output_array, data_length)

    # update boundary mask for new invalid entries that were replaced by despeckle
    for i in range(data_length):
        if input_list[i] != output_list[i]:
            boundary_mask_output[i] = True

    # returns the new data and masks packaged in an object
    return RadarData(output_list, boundary_mask_output)


def main():

    input_data = [-3.0, -3.0, -3.0, 5.0, 5.0, 5.0, -3.0, 5.0, 5.0, -3.0]
    bad = -3
    a_speckle = 3
    dgi_clip_gate = 10
    boundary_mask = [False, False, False, False, False, False, True, True, True, True]

    output_data = se_despeckle(input_data, bad, a_speckle, dgi_clip_gate, boundary_mask)
    assert (output_data.data == [-3.0, -3.0, -3.0, 5.0, 5.0, 5.0, -3.0, -3.0, -3.0, -3])
    print(output_data.mask)


# If executing script from shell, run the following code.
if __name__ == "__main__":
    print("PySolo Package Loaded")
    main()

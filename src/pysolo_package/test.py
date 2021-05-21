import ctypes
import os
import platform


dirname = os.path.dirname(os.path.abspath(__file__))
libraryName = os.path.join(dirname, 'libs/libSolo_18.04.so')
os.path.join(dirname, libraryName)
c_lib = ctypes.CDLL(libraryName)


def sampleAddInt(x, y):
    """ This function is to test the Solo SampleAddInt function from despeckle.cc, this returns the sum of two integers. """
    if not isinstance(x, int):
        raise ctypes.ArgumentError("Expected an integer for 1st parameter, received: %s " % x)
    elif not isinstance(y, int):
        raise ctypes.ArgumentError("Expected an integer for 2nd parameter, received: %s " % y)
    c_lib._Z12SampleAddIntii.argtypes = [ctypes.c_int]
    c_lib._Z12SampleAddIntii.restype = ctypes.c_int
    return c_lib._Z12SampleAddIntii(x, y)


def se_despeckle(input_data, bad, a_speckle, dgi_clip_gate, boundary_mask):
    """ 
        Args:
        input_data = float list,
        bad = float,
        a_speckle = int,
        dgi_clip_gate = int,
        boundary_mask = boolean list
        Returns:
        float list of output data
    """
    c_lib._Z12se_despecklePKfPfmfimPb.restype = None
    c_lib._Z12se_despecklePKfPfmfimPb.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.c_float, ctypes.c_int, ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]

    data_length = len(input_data)
    data_length_type = ctypes.c_float * data_length
    output_data = ctypes.cast(data_length_type(), ctypes.POINTER(ctypes.c_float))

    boundary_length_type = ctypes.c_bool * data_length

    c_lib._Z12se_despecklePKfPfmfimPb(data_length_type(*input_data), output_data, ctypes.c_size_t(data_length), ctypes.c_float(bad), ctypes.c_int(a_speckle), ctypes.c_size_t(dgi_clip_gate), boundary_length_type(*boundary_mask))

    output_list = [output_data[i] for i in range(len(input_data))]

    return output_list


def using_windows():
    """ This is to detect if the computer running this package is using Windows, which will not be compatible. """
    return platform.system() == "Windows"


def main():
    input_data = [1.0, 1.0, 1.0, 1.0, 1.0, 1000.0]
    bad = 3.5
    a_speckle = 80
    dgi_clip_gate = 8
    boundary_mask = [True, True, False, True, True, False]

    output_data = se_despeckle(input_data, bad, a_speckle, dgi_clip_gate, boundary_mask)
    print(output_data)


# If executing script from shell, run the following code.
if __name__ == "__main__":
    if (using_windows()):
        raise OSError('This system is using Windows. Windows is not compatible with LROSE functions.')
    else:
        print("PySolo Package Loaded")
        main()

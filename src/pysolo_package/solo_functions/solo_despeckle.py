import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, tasks
from pysolo_package.utils.function_alias import aliases

se_despeckle = aliases['despeckle']

def despeckle(input_list, bad, a_speckle, dgi_clip_gate, boundary_mask_input, boundary_mask_all_true=False):
	if (len(input_list) != len(boundary_mask_input)):
		raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(boundary_mask_input)))

	# set return type and arg types
	se_despeckle.restype = None
	se_despeckle.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.c_float, ctypes.c_int, ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]

	boundary_mask_output = deepcopy(boundary_mask_input)

	# retrieve size of input/output/mask array
	data_length = len(input_list)
	# create a ctypes type that is an array of floats of length from above
	data_length_type = ctypes.c_float * data_length
	# initialize an empty float array of length
	output_array = tasks.initialize_float_array(data_length)

	# create a ctypes type that is an array of bools of length from above
	boundary_length_type = ctypes.c_bool * data_length

	# if optional, last parameter set to True, then create a list of bools set to True of length from above
	if boundary_mask_all_true:
		boundary_mask_input = [True] * data_length

	# run C function, output_array is updated with despeckle results
	se_despeckle(data_length_type(*input_list), output_array, ctypes.c_size_t(data_length), ctypes.c_float(bad), ctypes.c_int(a_speckle), ctypes.c_size_t(dgi_clip_gate), boundary_length_type(*boundary_mask_input))

	# convert ctypes array to python list
	output_list = tasks.array_to_list(output_array, data_length)

	boundary_mask_output = tasks.update_boundary_mask(input_list, output_list, boundary_mask_output)

	# returns the new data and masks packaged in an object
	return radar_structure.RadarData(output_list, boundary_mask_output)
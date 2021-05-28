from pysolo_package.solo_functions.solo_despeckle import despeckle
from pysolo_package.solo_functions.solo_ring_zap import ring_zap

input_data = [3, 4, 5, 6]
bad = -3
a_speckle = 1
dgi_clip_gate = 4
boundary_mask = [True, True, True, True]
despeckle(input_data, bad, a_speckle, dgi_clip_gate, boundary_mask)
print("A")

from_km = 2
to_km = 9
input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
bad = -3
dgi_clip_gate = 10
boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]
expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
output_data = ring_zap(from_km, to_km, input_data, bad, dgi_clip_gate, boundary_mask)
assert (output_data.data == expected_data)
print("B")

# If executing script from shell, run the following code.
if __name__ == "__main__":
	print("PySolo Package Loaded")


# This file is to test features from the package
# Pip install from here to test:
# https://test.pypi.org/project/pysolo-wip/

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RadarData
from pysolo_package.utils.enums import Where

# test despeckle
input_data = [3, -3, -3, 5, 5, 5, -3, 5, 5, -3]
bad = -3
a_speckle = 3
dgi_clip_gate = 8
boundary_mask = [True, True, True, True, True, True, True, True, True, True]
expected_data = [-3, -3, -3, -3, -3, -3, -3, 5, 5, -3]
output = solo.despeckle(input_data, bad, a_speckle, boundary_mask, dgi_clip_gate)
assert output.data == expected_data
print("A")

# test ring zap
from_km = 2
to_km = 9
input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
bad = -3
dgi_clip_gate = 10
boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]
expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
output_data = solo.ring_zap(from_km, to_km, input_data, bad, boundary_mask, 10)
assert (output_data.data == expected_data)
print("B")

# test threshold
input_data =    [-3,  4,  6, -3,  8,  -3, 10,  12, 14, -3, -3 ]
thr_data =      [-5, 30, 40, 60, -5,  70, -5, 110, -5, 10, 140]
expected_data = [-3, -3, -3, -3, -3, -3, -3, 12, -3, -3, -3]

bad = -3
thr_bad = -5

boundary_mask = [True, True, True, True, True, True, True, True, True, True, True]

output_data = solo.threshold(Where.BELOW.value, 50, 0.000, 0, input_data, thr_data, bad, thr_bad, boundary_mask)
assert output_data.data == expected_data
print("E")

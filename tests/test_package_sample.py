# This file is to test features from the package
# Pip install from here to test:
# https://test.pypi.org/project/pysolo-wip/

import numpy as np

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RayData
from pysolo_package.utils.enums import Where

# test despeckle
input_data = [3, -3, -3, 5, 5, 5, -3, 5, 5, -3]
bad = -3
a_speckle = 3
dgi = 8
input_boundary_mask = [True, True, True, True, True, True, True, True, True, True]
expected_data = [-3, -3, -3, -3, -3, -3, -3, 5, 5, -3]
output = solo.despeckle(input_data, bad, a_speckle, dgi_clip_gate=dgi, boundary_mask=input_boundary_mask)
assert output.data == expected_data


# test ring zap
input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
bad = -3
from_km = 2
to_km = 9
dgi = 10
input_boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]
expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
output_data = solo.ring_zap(input_data, bad, from_km, to_km, dgi_clip_gate=dgi, boundary_mask=input_boundary_mask)
assert (output_data.data == expected_data)


# test threshold
input_data =    [-3,  4,  6, -3,  8,  -3, 10,  12, 14, -3, -3 ]
thr_data =      [-5, 30, 40, 60, -5,  70, -5, 110, -5, 10, 140]
expected_data = [-3, -3, -3, -3, -3, -3, -3, 12, -3, -3, -3]
bad = -3
thr_bad = -5
input_boundary_mask = [True, True, True, True, True, True, True, True, True, True, True]
output_data = solo.threshold(input_data, thr_data, bad, Where.BELOW.value, 50, 0, thr_missing=thr_bad, boundary_mask=input_boundary_mask)
assert output_data.data == expected_data


# test flag_glitches
input_data = [3, 4, 5, -6, -7, 4, 4, 5]
input_boundary_mask = [True, True, True, True, True, True, True, True]
input_bad_flag = [False, False, False, False, True, True, True, True]
bad = -3
deglitch_threshold = 3
deglitch_radius = 1
deglitch_min_bins = 3
expected_bad_flag = [False, False, True, False, True, True, True, True]
output_bad_flag = solo.flag_glitches(input_data, bad, deglitch_threshold, deglitch_radius, deglitch_min_bins, input_bad_flag, boundary_mask=input_boundary_mask)
assert (output_bad_flag.mask == expected_bad_flag)


# test unfold_local_wind
data = [3, 4, 5, 6]
bad = -3
ngates_averaged = 3
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 10.0
dds_radd_eff_unamb_vel = 0.0
azimuth_angle_degrees = 360.0
elevation_angle_degrees = 90.0
ew_horiz_wind = 999
ns_horiz_wind = 999
vert_wind = 2.0
expected_data = [3.0, 4.0, 5.0, 6.0]
output_data = solo.unfold_local_wind(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_horiz_wind, ns_horiz_wind, vert_wind, max_pos_folds, max_neg_folds, ngates_averaged)
assert (output_data.data == expected_data)

data = [3,-3, -3, 5, 5,-2, -3, 5, 5, -3]
boundary = [True, False,  True, True, False, True,  True, True, True, False]
bad = -3
dgi = 8
ngates_averaged = 1
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 10.0
dds_radd_eff_unamb_vel = 0.0
azimuth_angle_degrees = 360.0
elevation_angle_degrees = 90.0
ew_horiz_wind = 999
ns_horiz_wind = 999
vert_wind = 3.0
expected_data = [3,-3, -3, 5, 5,-2, -3, 5, 5, -3]
output_data = solo.unfold_local_wind(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_horiz_wind, ns_horiz_wind, vert_wind, max_pos_folds, max_neg_folds, ngates_averaged, dgi_clip_gate= dgi, boundary_mask = boundary)
assert (output_data.data == expected_data)


# test unfold_first_good_gate
data = [3, 4, 5, 6]
bad = -3
ngates_averaged = 3
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 10.0
dds_radd_eff_unamb_vel = 0.0
expected_data = [3.0, 4.0, 5.0, 6.0]
last_good_v0 = [bad]
output_data = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
assert (output_data.data == expected_data), output_data.data

data = [-3, -3, 5, 6]
input_boundary_mask = [True, True, True, True]
bad = -3
ngates_averaged = 3
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 10.0
dds_radd_eff_unamb_vel = 0.0
expected_data = [-3, -3, 5, 6]
last_good_v0 = [bad]
output_data = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
assert (output_data.data == expected_data)

data = [3, 4, 5, 6]
input_boundary_mask = [True, True, True, True]
bad = -3
ngates_averaged = 3
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 10.0
dds_radd_eff_unamb_vel = 0.0
expected_data = [3, 4, 5, 6]
last_good_v0 = [9]
output_data = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
assert (output_data.data == expected_data)

data = [3, -3, 5, -16, 7, -3 ,6]
boundary = [False, False, True, True, False, True, True]
bad = -3
ngates_averaged = 2
max_pos_folds = 5
max_neg_folds = 5
nyquist_velocity = 3.2
dds_radd_eff_unamb_vel = 0.0
expected_data = [3, -3, 5, 2, 7, -3, 6]
last_good_v0 = [bad]
output_data = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, boundary_mask = boundary)
assert (output_data.data == expected_data), output_data.data

# test radial shear
seds_gate_diff_interval = 4
data = [-3, 4, 5, 6, 7, 8, 9, 10]
nGates = 8
bad_data_value = -3
dgi = 8
boundary_mask = [True, True, True, True, True, True, True, True]
expected_data = [-3, 4, 4, 4, 0, 0, 0, 0]
output_data = solo.radial_shear(data, bad, seds_gate_diff_interval)
assert (output_data.data == expected_data), output_data.data

seds_gate_diff_interval = 5
data = [8, -3, -3, -3, 4, 8, 6, 4, 4, -3, 2, 3]
nGates = 12
bad_data_value = -3
dgi = 10
boundary_mask = [True, True, True, True, True, False, False, False, True, True, True, True]
expected_data = [0, -3, -3, -3, -3, 0, 0, 0, 0, 0, 0, 0]
output_data = solo.radial_shear(data, bad, seds_gate_diff_interval, dgi_clip_gate=dgi)
assert (output_data.data == expected_data), output_data.data

seds_gate_diff_interval = 30
data = [8, -3, -3, -3, 4, 8, 6, 4, 4, -3, 2, 3]
nGates = 12
bad_data_value = -3
dgi = 10
boundary_mask = [True, True, True, True, True, False, False, False, True, True, True, True]
expected_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
output_data = solo.radial_shear(data, bad, seds_gate_diff_interval, dgi_clip_gate=dgi)
assert (output_data.data == expected_data), output_data.data

# test rain rate
# for any good values 'g', sets it to g = (1/300) * 10 ^ (0.1 * g * d_const)
d_const = 4
data = [8, -3, -3, -3, 4, 8, 6, 4, 4, -3, 2, 3]
nGates = 12
bad_data_value = -3
boundary_mask = [True, True, True, True, True, True, True, True, True, True, True, True]
expected_data = [5.282977308, -3, -3, -3, 0.1327023902, 5.282977308, 0.8372954772, 0.1327023902, 0.1327023902, -3, 0.02103191148, 0.05282977308]
output_data = solo.rain_rate(data, bad, d_const)
assert (np.allclose(output_data.data, expected_data))

print("All tests passed.")

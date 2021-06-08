# This file is to test features from the package
# Pip install from here to test:
# https://test.pypi.org/project/pysolo-wip/

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RadarData
from pysolo_package.utils.enums import Where


# # test despeckle
# input_data = [3, -3, -3, 5, 5, 5, -3, 5, 5, -3]
# bad = -3
# a_speckle = 3
# dgi_clip_gate = 8
# input_boundary_mask = [True, True, True, True, True, True, True, True, True, True]
# expected_data = [-3, -3, -3, -3, -3, -3, -3, 5, 5, -3]
# output = solo.despeckle(input_data, bad, a_speckle, input_boundary_mask, dgi_clip_gate)
# assert output.data == expected_data
# print("A")


# # test ring zap
# from_km = 2
# to_km = 9
# input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
# bad = -3
# dgi_clip_gate = 10
# input_boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]
# expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
# output_data = solo.ring_zap(from_km, to_km, input_data, bad, input_boundary_mask, 10)
# assert (output_data.data == expected_data)
# print("B")


# # test threshold
# input_data =    [-3,  4,  6, -3,  8,  -3, 10,  12, 14, -3, -3 ]
# thr_data =      [-5, 30, 40, 60, -5,  70, -5, 110, -5, 10, 140]
# expected_data = [-3, -3, -3, -3, -3, -3, -3, 12, -3, -3, -3]
# bad = -3
# thr_bad = -5
# input_boundary_mask = [True, True, True, True, True, True, True, True, True, True, True]
# output_data = solo.threshold(Where.BELOW.value, 50, 0, input_data, thr_data, bad, input_boundary_mask, thr_missing=thr_bad)
# assert output_data.data == expected_data
# print("C")


# # test flag_glitches
# input_data = [3, 4, 5, -6, -7, 4, 4, 5]
# input_boundary_mask = [True, True, True, True, True, True, True, True]
# input_bad_flag = [False, False, False, False, True, True, True, True]
# bad = -3
# deglitch_threshold = 3
# deglitch_radius = 1
# deglitch_min_bins = 3
# expected_bad_flag = [False, False, True, False, True, True, True, True]
# output_bad_flag = solo.flag_glitches(deglitch_threshold, deglitch_radius, deglitch_min_bins, input_data, bad, input_boundary_mask, input_bad_flag)
# assert (output_bad_flag.data == expected_bad_flag)
# print("D")

import pyart
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

radar = pyart.io.read("C:/Users/Marma/Desktop/pysolo/tests/radar_data.nc")
print(list(radar.fields.keys()))

a_speckle = 2
despeckled_mask_B = solo.despeckle_masked(radar.fields['ZZ']['data'], a_speckle)

from_km = 5
to_km = 6
kilometers_between_gates = radar.range['meters_between_gates'] / 1000
ring_zapped_mask_B = solo.ring_zap_masked(radar.fields['ZZ']['data'], from_km, to_km, kilometers_between_gates)

radar.add_field_like('ZZ', 'ZZ_despeckled', despeckled_mask_B,   replace_existing=True)
radar.add_field_like('ZZ', 'ZZ_ring_zapped', ring_zapped_mask_B, replace_existing=True)

display = pyart.graph.RadarMapDisplay(radar)

fig = plt.figure(figsize=(14, 14))

ax = fig.add_subplot(221)
display.plot_ppi(field='ZZ', vmin=-40, vmax=40, title="Original (PPI)", cmap='pyart_NWSRef')
display.set_limits((-20, 20), (-5, 25), ax=ax)

ax = fig.add_subplot(222)
display.plot_ppi(field='ZZ_despeckled', vmin=-40, vmax=40, title="Despeckled (PPI)", cmap='pyart_NWSRef')
display.set_limits((-20, 20), (-5, 25), ax=ax)

ax = fig.add_subplot(223)
display.plot(field='ZZ', vmin=-40, vmax=40, title="Original (RHI)", cmap='pyart_NWSRef')
display.set_limits((-50, 50), (-10, 35), ax=ax)

ax = fig.add_subplot(224)
display.plot(field='ZZ_despeckled', vmin=-40, vmax=40, title="Despeckled (RHI)", cmap='pyart_NWSRef')
display.set_limits((-50, 50), (-10, 35), ax=ax)

ax = fig.add_subplot(221)
display.plot_ppi(field='ZZ', vmin=-40, vmax=40, title="Original (PPI)", cmap='pyart_NWSRef')

display.set_limits((-20, 20), (-5, 25), ax=ax)

ax = fig.add_subplot(222)
display.plot_ppi(field='ZZ_ring_zapped', vmin=-40, vmax=40, title="Ring Zapped (PPI)", cmap='pyart_NWSRef')
display.set_limits((-20, 20), (-5, 25), ax=ax)

ax = fig.add_subplot(223)
display.plot(field='ZZ', vmin=-40, vmax=40, title="Original", cmap='pyart_NWSRef')

display.set_limits((-50, 50), (-10, 35), ax=ax)

ax = fig.add_subplot(224)
display.plot(field='ZZ_ring_zapped', vmin=-40, vmax=40, title="Ring Zapped", cmap='pyart_NWSRef')
display.set_limits((-50, 50), (-10, 35), ax=ax)

plt.suptitle('Ring Zap', fontsize=16)
plt.show()

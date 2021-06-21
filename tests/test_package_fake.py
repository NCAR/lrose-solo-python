import pyart
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from copy import *

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RayData
from pysolo_package.utils.enums import Where
import os
import math
import random

os.system("cls")

radius = 150

data = []
mask = []


for i in range(360):
    data.append([10] * 627)
    mask.append([True] * 627)

for i in range(0, 1440, 1):
    x = math.cos(math.radians(i/4)) * radius 
    y = math.sin(math.radians(i/4)) * radius 
    mask[round(radius-y)+30][round(radius-x)] = False
    # if (20 < i < 35):
    #     x = math.cos(math.radians(i)) * (radius)
    #     y = math.sin(math.radians(i)) * (radius)
    #     for j in range(10):
    #         data[round(radius+y+j)][round(radius+x)] = -40
    #         mask[round(radius+y+j)][round(radius+x)] = False
    # if (90 < i < 270):
    #     x = math.cos(math.radians(i)) * (radius / 4)
    #     y = math.sin(math.radians(i)) * (radius / 4)
    #     for j in range(20):
    #         data[round(radius-y+j)][round(radius-x+j)] = 80
    #         mask[round(radius-y+j)][round(radius-x+j)] = False


# random_num = 228
# random_x = -2
# random_y = 8
# for i in range(10):
#     for j in range(random_num - 10, random_num + 10):
#             data[random_y + j][random_x + j] = 40
#             mask[random_y + j][random_x + j] = False      


for i in range(len(mask)):
    try:
        first_index = mask[i].index(False)
        reversed_list = mask[i][::-1]
        first_index_in_reversed = reversed_list.index(False)
        last_index = len(mask[i]) -1 - first_index_in_reversed
    except ValueError:
        continue

    for j in range(first_index, last_index + 1):
        mask[i][j] = False


masked_array = np.ma.masked_array(data=data, mask=mask, fill_value=0)
radar = pyart.io.read("C:/Users/Marma/Desktop/pysolo/tests/radar_data.nc")
mask_dict = {'data': masked_array, 'long_name': 'test',
             '_FillValue': masked_array.fill_value, 'standard_name': 'test'}
radar.add_field('test', mask_dict)

############ [Despeckle] ##############
a_speckle = 2
despeckled_mask = solo.despeckle_masked(radar.fields['test']['data'], a_speckle)
radar.add_field_like('test', 'test_despeckled', despeckled_mask, replace_existing=True)

############# [Ring Zap] ##############
from_km = 5
to_km = 6
kilometers_between_gates = radar.range['meters_between_gates'] / 1000
ring_zapped_mask = solo.ring_zap_masked(radar.fields['test']['data'], from_km, to_km, kilometers_between_gates)
radar.add_field_like('test', 'test_zapped', ring_zapped_mask, replace_existing=True)

############# [Deglitch] ##############
deglitch_threshold = 1
deglitch_radius = 25
deglitch_min_bins = 20
bad_flag_mask_before = copy(radar.fields['test']['data'].mask.tolist())
flag_glitches_mask = solo.flag_glitches_masked(radar.fields['test']['data'], bad_flag_mask_before, deglitch_threshold, deglitch_radius, deglitch_min_bins, boundary_mask_all_true=True)
radar.add_field_like('test', 'test_deglitched', flag_glitches_mask, replace_existing=True)


display = pyart.graph.RadarMapDisplay(radar)
fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(221)
display.plot(field='test', vmin=-40, vmax=40, title="Original", cmap='pyart_NWSRef')
display.set_limits((-16, 0), (-2, 6), ax=ax)
ax = fig.add_subplot(222)
display.plot(field='test_deglitched', vmin=-40, vmax=40, title="After Deglitch", cmap='pyart_NWSRef')
display.set_limits((-16, 0), (-2, 6), ax=ax)
ax = fig.add_subplot(223)
display.plot(field='test_despeckled', vmin=-40, vmax=40, title="After Despeckle", cmap='pyart_NWSRef')
display.set_limits((-16, 0), (-2, 6), ax=ax)
ax = fig.add_subplot(224)
display.plot(field='test_zapped', vmin=-40, vmax=40, title="After Ring Zapped", cmap='pyart_NWSRef')
display.set_limits((-16, 0), (-2, 6), ax=ax)
plt.show()


# x = (np.linspace(start=0, stop=359, num=360))
# plt.plot(x, masked_array)
# plt.show()
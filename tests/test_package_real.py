
import pyart
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from copy import *
import sys
import pprint

import pysolo_package as solo
from pysolo_package.solo_functions.solo_flag_freckles import flag_freckles
from pysolo_package.utils.radar_structure import RadarData
from pysolo_package.utils.enums import Where

radar = pyart.io.read("C:/Users/Marma/Desktop/pysolo/tests/radar_data.nc")

############ [Despeckle] ##############
a_speckle = 2
ZZ_masked_array = radar.fields['ZZ']['data']
despeckled_mask = solo.despeckle_masked(ZZ_masked_array, a_speckle)
radar.add_field_like('ZZ', 'ZZ_despeckled', despeckled_mask,   replace_existing=True)

############# [Ring Zap] ##############
from_km = 5
to_km = 6
kilometers_between_gates = radar.range['meters_between_gates'] / 1000
ring_zapped_mask = solo.ring_zap_masked(radar.fields['ZZ']['data'], from_km, to_km, kilometers_between_gates)
radar.add_field_like('ZZ', 'ZZ_ring_zapped', ring_zapped_mask, replace_existing=True)

############ [Threshold] ##############
thr_1 =  -7
thr_2 = 0
threshold_mask = solo.threshold_masked(radar.fields['ZZ']['data'], radar.fields['VV']['data'], solo.Where.BELOW.value, thr_1, thr_2)
radar.add_field_like('ZZ', 'ZZ_threshold', threshold_mask, replace_existing=True)

############# [Deglitch] ##############
deglitch_threshold = 1
deglitch_radius = 20
deglitch_min_bins = 27
bad_flag_mask = copy(radar.fields['ZZ']['data'].mask.tolist())
flag_glitches_mask = solo.flag_glitches_masked(radar.fields['ZZ']['data'], bad_flag_mask, deglitch_threshold, deglitch_radius, deglitch_min_bins, boundary_mask_all_true=True)
radar.add_field_like('ZZ', 'ZZ_flag_glitch', flag_glitches_mask, replace_existing=True)

############## [Freckles] ##############
freckle_threshold = 4
freckle_avg_count = 4
bad_flag_mask = copy(radar.fields['ZZ']['data'].mask.tolist())
flag_freckles_mask = solo.flag_freckles_masked(radar.fields['ZZ']['data'], bad_flag_mask, freckle_threshold, freckle_avg_count, boundary_mask_all_true=True)
radar.add_field_like('ZZ', 'ZZ_flag_freckles', flag_freckles_mask, replace_existing=True)

display = pyart.graph.RadarMapDisplay(radar)

def demoDespeckle(display):
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
    plt.suptitle('Despeckle', fontsize=16)
    plt.show()


def demoRing(display):
    fig = plt.figure(figsize=(14, 14))
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


def demoThreshold(display):
    display = pyart.graph.RadarMapDisplay(radar)
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(221)
    display.plot_ppi(field='ZZ', vmin=-20, vmax=10, title="Original (ZZ) (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(222)
    display.plot_ppi(field='ZZ_threshold', vmin=-20, vmax=10, title="Threshold (ZZ) (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(223)
    display.plot_ppi(field='VV', vmin=-20, vmax=10, title="Original (VV) (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    plt.show()


def demoFlagGlitches(display):
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(221)
    display.plot_ppi(field='ZZ', vmin=-40, vmax=40, title="Original (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(222)
    display.plot_ppi(field='ZZ_flag_glitch', vmin=-40, vmax=40, title="Flag Glitch (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(223)
    display.plot(field='ZZ', vmin=-40, vmax=40, title="Original", cmap='pyart_NWSRef')
    display.set_limits((-50, 50), (-10, 35), ax=ax)
    ax = fig.add_subplot(224)
    display.plot(field='ZZ_flag_glitch', vmin=-40, vmax=40, title="Flag Glitch", cmap='pyart_NWSRef')
    display.set_limits((-50, 50), (-10, 35), ax=ax)
    plt.suptitle('Flag Glitch | deglitch_threshold = %d, deglitch_radius = %d deglitch_min_bins = %d' % (deglitch_threshold, deglitch_radius, deglitch_min_bins), fontsize=16)
    plt.show()

def demoFlagFreckles(display):
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(221)
    display.plot_ppi(field='ZZ', vmin=-40, vmax=40, title="Original (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(222)
    display.plot_ppi(field='ZZ_flag_freckles', vmin=-40, vmax=40, title="Flag Freckles (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(223)
    display.plot(field='ZZ', vmin=-40, vmax=40, title="Original (RHI)", cmap='pyart_NWSRef')
    display.set_limits((-50, 50), (-10, 35), ax=ax)
    ax = fig.add_subplot(224)
    display.plot(field='ZZ_flag_freckles', vmin=-40, vmax=40, title="Flag Freckles (RHI)", cmap='pyart_NWSRef')
    display.set_limits((-50, 50), (-10, 35), ax=ax)
    plt.suptitle('Flag Glitch | freckle_threshold = %d, freckle_avg_count = %d' % (freckle_threshold, freckle_avg_count), fontsize=16)
    plt.show()


# demoDespeckle(display)
# demoRing(display)
# demoThreshold(display)
# demoFlagGlitches(display)
demoFlagFreckles(display)

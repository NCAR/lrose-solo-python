from numpy.ma.core import masked_equal
import pyart
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import src.pysolo as solo # pylint: disable=import-error


path_to_file = Path.cwd() / Path('tests/data/radar_data_a.nc')

radar = pyart.io.read(path_to_file)

############ [Despeckle] ##############
a_speckle = 2
ZZ_masked_array = radar.fields['ZZ']['data']
despeckled_mask = solo.despeckle_masked(ZZ_masked_array, a_speckle)
radar.add_field_like('ZZ', 'ZZ_despeckled', despeckled_mask, replace_existing=True)

# ############# [Ring Zap] ##############
from_km = 25
to_km = 30
kilometers_between_gates = radar.range['meters_between_gates'] / 1000
ring_zapped_mask = solo.ring_zap_masked(
    radar.fields['ZZ']['data'], from_km, to_km, kilometers_between_gates)
radar.add_field_like('ZZ', 'ZZ_ring_zapped',
                     ring_zapped_mask, replace_existing=True)

# ############ [Threshold] ##############
thr_1 = -7
thr_2 = 0
threshold_mask = solo.threshold_masked(radar.fields['ZZ']['data'], radar.fields['VV']['data'], solo.Where.BELOW.value, thr_1, thr_2)
radar.add_field_like('ZZ', 'ZZ_threshold', threshold_mask, replace_existing=True)

# ########### [Merge Fields] #############
# This function works but can't really be demonstrated with this data
thr_1 =  -7
thr_2 = 0
threshold_mask = solo.merge_fields_masked(radar.fields['ZZ']['data'], radar.fields['VV']['data'])
radar.add_field_like('ZZ', 'ZZ_merge', threshold_mask, replace_existing=True)

# ############# [Deglitch] ##############
deglitch_threshold = 1
deglitch_radius = 20
deglitch_min_bins = 27
flag_glitches_mask = solo.flag_glitches_masked(
    radar.fields['ZZ']['data'], deglitch_threshold, deglitch_radius, deglitch_min_bins)
radar.add_field_like('ZZ', 'ZZ_flag_glitch',
                     flag_glitches_mask, replace_existing=True)

# ############## [Freckles] ##############
freckle_threshold = 12
freckle_avg_count = 2
flag_freckles_mask = solo.flag_freckles_masked(
    radar.fields['ZZ']['data'], freckle_threshold, freckle_avg_count)
radar.add_field_like('ZZ', 'ZZ_flag_freckles',
                     flag_freckles_mask, replace_existing=True)

# ########## [Forced unfolding] ##########
nyquist_velocity = 30
dds_radd_eff_unamb_vel = 0
center = 0
forced_unfolding_mask = solo.forced_unfolding_masked(
    radar.fields['VV']['data'], nyquist_velocity, dds_radd_eff_unamb_vel, center)
radar.add_field_like('VV', 'VV_forced_unfolding',
                     forced_unfolding_mask, replace_existing=True)

# ####### [Unfold First Good Gate] #######
nyquist_velocity = 25
dds_radd_eff_unamb_vel = 5
max_pos_folds = 10
max_neg_folds = 10
ngates_averaged = 20
last_good_v0 = [1] * radar.ngates
BB_unfolding_fgg_mask = solo.unfold_first_good_gate_masked(
    radar.fields['VV']['data'], nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
radar.add_field_like('VV', 'VV_unfold_first_good_gate',
                     BB_unfolding_fgg_mask, replace_existing=True)

# ######### [Unfold Local Wind] ##########
nyquist_velocity = 25
dds_radd_eff_unamb_vel = 5
azimuth_angle_degrees = 5
elevation_angle_degrees = 5
ew_wind = 5
ns_wind = 5
ud_wind = 5
max_pos_folds = 10
max_neg_folds = 10
ngates_averaged = 20
BB_unfolding_lw_mask = solo.unfold_local_wind_masked(radar.fields['VV']['data'], nyquist_velocity, dds_radd_eff_unamb_vel,
                                                     azimuth_angle_degrees, elevation_angle_degrees, ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged)
radar.add_field_like('VV', 'VV_unfold_local_wind',
                     BB_unfolding_lw_mask, replace_existing=True)

############ [Radial Shear] #############
seds_gate_diff_interval = round(radar.ngates / 2)
radial_shear_mask = solo.radial_shear_masked(
    radar.fields['ZZ']['data'], seds_gate_diff_interval)
radar.add_field_like('ZZ', 'ZZ_radial_shear',
                     radial_shear_mask, replace_existing=True)  # velocity

############## [Rain Rate] ##############
# for any good values 'g', sets it to g = (1/300) * 10 ^ (0.1 * g * d_const)
d_const = 6
rain_rate_mask = solo.rain_rate_masked(radar.fields['VV']['data'], d_const)
radar.add_field_like('VV', 'VV_rain_rate', rain_rate_mask,
                     replace_existing=True)

display = pyart.graph.RadarMapDisplay(radar)


def graphPlot(plot_field, ref='ZZ'):
    fig, ax = plt.subplots(ncols=2, figsize=(15, 7))
    display.plot(field=ref, vmin=-40, vmax=40, title=ref,
                 cmap='pyart_NWSRef', ax=ax[0])
    display.set_limits((-50, 50), (-10, 35), ax=ax[0])
    display.plot(field=plot_field, vmin=-40, vmax=40,
                 title=plot_field, cmap='pyart_NWSRef', ax=ax[1])
    display.set_limits((-50, 50), (-10, 35), ax=ax[1])
    plt.suptitle(plot_field, fontsize=16)
    plt.show()


def demoThreshold(test_field):
    display = pyart.graph.RadarMapDisplay(radar)
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(221)
    display.plot(field='ZZ', vmin=-20, vmax=10,
                 title="Original (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(222)
    display.plot(field=test_field, vmin=-20, vmax=10,
                 title=f"{test_field} (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    ax = fig.add_subplot(223)
    display.plot(field='VV', vmin=-20, vmax=10,
                 title="Original (VV) (PPI)", cmap='pyart_NWSRef')
    display.set_limits((-20, 20), (-5, 25), ax=ax)
    plt.show()


graphPlot('ZZ_despeckled')
graphPlot('ZZ_ring_zapped')
demoThreshold('ZZ_threshold')
demoThreshold('ZZ_merge')
graphPlot('ZZ_flag_glitch')
graphPlot('ZZ_flag_freckles')
graphPlot('VV_forced_unfolding', 'VV')
graphPlot('VV_unfold_first_good_gate', 'VV')
graphPlot('VV_unfold_local_wind', 'VV')
graphPlot('ZZ_radial_shear', 'ZZ')
graphPlot('VV_rain_rate', 'VV')

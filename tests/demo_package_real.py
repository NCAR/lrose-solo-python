import src.pysolo as solo 
import timeit
from numpy.ma.core import masked_equal
import pyart
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


path_to_file = Path.cwd() / Path('tests/data/radar_data_c.nc')
field = 'reflectivity'
field_ref = 'velocity'
radar = pyart.io.read(path_to_file)
print(radar.fields.keys())

############ [Despeckle] ##############
starttime = timeit.default_timer()
a_speckle = 2
solo.despeckle_field(radar, field, f'{field}_despeckled', a_speckle)
print("Despeckle Finished:", timeit.default_timer() - starttime)

# ############# [Ring Zap] ##############
starttime = timeit.default_timer()
from_km = 25
to_km = 30
kilometers_between_gates = radar.range['meters_between_gates'] / 1000
ring_zapped_mask = solo.ring_zap_masked(
    radar.fields[field]['data'], from_km, to_km, kilometers_between_gates)
radar.add_field_like(field, f'{field}_ring_zapped',
                     ring_zapped_mask, replace_existing=True)
print("Ring Zap Finished:", timeit.default_timer() - starttime)


# ############ [Threshold] ##############
starttime = timeit.default_timer()
thr_1 = -7
thr_2 = 0
solo.threshold_fields(radar, field, field_ref, f'{field}_threshold', solo.Where.BELOW, thr_1, thr_2)
print("Threshold Finished:", timeit.default_timer() - starttime)

exit(0)

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
ew_wind = 5
ns_wind = 5
ud_wind = 5
max_pos_folds = 10
max_neg_folds = 10
ngates_averaged = 20
solo.unfold_local_wind_fields(radar, 'VV', 'VV_unfold_local_wind', ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged)

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
    plt.savefig('quick-test2.png')
    # plt.show()


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
    plt.savefig('quick-test2.png')


# graphPlot('ZZ_despeckled')
# graphPlot('ZZ_ring_zapped')
# demoThreshold('ZZ_threshold')
# demoThreshold('ZZ_merge')
# graphPlot('ZZ_flag_glitch')
# graphPlot('ZZ_flag_freckles')
# graphPlot('VV_forced_unfolding', 'VV')
# graphPlot('VV_unfold_first_good_gate', 'VV')
# graphPlot('VV_unfold_local_wind', 'VV')
# graphPlot('ZZ_radial_shear', 'ZZ')
# graphPlot('VV_rain_rate', 'VV')

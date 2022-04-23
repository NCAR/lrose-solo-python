import timeit
from pathlib import Path
import pyart
import matplotlib.pyplot as plt
import src.pysolo as solo


class TestPlots:

    def __init__(self, pathToData, test_field, test_field_ref, showGraphs=False) -> None:
        self.radar = pyart.io.read(pathToData)
        self.test_field = test_field
        self.test_field_ref = test_field_ref
        self.display = pyart.graph.RadarMapDisplay(self.radar)
        self.graph = showGraphs
        print(list(self.radar.fields.keys()))
        print("Number of rays:", self.radar.nrays)
        print("Number of gates:", self.radar.ngates)


    def graphPlot(self, plot_field):
        if self.graph:
            _, ax = plt.subplots(ncols=2, figsize=(15, 7))
            self.display.plot(field=self.test_field, vmin=-40, vmax=40, title=self.test_field, cmap='pyart_NWSRef', ax=ax[0])
            self.display.set_limits((-50, 50), (-10, 35), ax=ax[0])
            self.display.plot(field=plot_field, vmin=-40, vmax=40, title=plot_field, cmap='pyart_NWSRef', ax=ax[1])
            self.display.set_limits((-50, 50), (-10, 35), ax=ax[1])
            plt.suptitle(plot_field, fontsize=16)
            plt.show()
            plt.savefig('quick-test2.png')


    def demoThreshold(self, result_field):
        if self.graph:
            fig = plt.figure(figsize=(14, 14))
            ax = fig.add_subplot(221)
            self.display.plot(field=self.test_field, vmin=-10, vmax=30, title=f"Original ({self.test_field}) (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            ax = fig.add_subplot(222)
            self.display.plot(field=result_field, vmin=-10, vmax=30, title=f"{result_field} (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            ax = fig.add_subplot(223)
            self.display.plot(field=self.test_field_ref, vmin=-10, vmax=30, title=f"Original ({self.test_field_ref}) (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            plt.show()


    ############ [Despeckle] ##############
    def test_despeckle(self):
        a_speckle = 5
        solo.despeckle_field(self.radar, self.test_field, f'{self.test_field}_despeckled', a_speckle)
        self.graphPlot(f'{self.test_field}_despeckled')


    # ############# [Ring Zap] ##############
    def test_ring_zap(self):
        from_km = 25
        to_km = 30
        kilometers_between_gates = self.radar.range['meters_between_gates'] / 1000
        ring_zapped_mask = solo.ring_zap_masked(
            self.radar.fields[self.test_field]['data'], from_km, to_km, kilometers_between_gates)
        self.radar.add_field_like(self.test_field, f'{self.test_field}_ring_zapped',
                            ring_zapped_mask, replace_existing=True)
        self.graphPlot('ZZ_ring_zapped')


    # ############ [Threshold] ##############
    def test_threshold(self):
        thr_1 = -1
        thr_2 = 0
        solo.threshold_fields(self.radar, self.test_field, self.test_field_ref, f'{self.test_field}_threshold', solo.Where.BELOW, thr_1, thr_2)
        self.demoThreshold(f'{self.test_field}_threshold')


    # ########### [Merge Fields] #############
    # This function works but can't really be demonstrated with this data
    def test_merge(self):
        threshold_mask = solo.merge_fields_masked(self.radar.fields['ZZ']['data'], self.radar.fields['VV']['data'])
        self.radar.add_field_like('ZZ', 'ZZ_merge', threshold_mask, replace_existing=True)
        self.graphPlot('ZZ_merge')


    # ############# [Deglitch] ##############
    def test_deglitch(self):
        deglitch_threshold = 1
        deglitch_radius = 20
        deglitch_min_bins = 27
        flag_glitches_mask = solo.flag_glitches_masked(
            self.radar.fields['ZZ']['data'], deglitch_threshold, deglitch_radius, deglitch_min_bins)
        self.radar.add_field_like('ZZ', 'ZZ_flag_glitch',
                            flag_glitches_mask, replace_existing=True)
        self.graphPlot('ZZ_flag_glitch')


    # ############## [Freckles] ##############
    def test_freckles(self):
        freckle_threshold = 12
        freckle_avg_count = 2
        flag_freckles_mask = solo.flag_freckles_masked(
            self.radar.fields['ZZ']['data'], freckle_threshold, freckle_avg_count)
        self.radar.add_field_like('ZZ', 'ZZ_flag_freckles',
                            flag_freckles_mask, replace_existing=True)
        self.graphPlot('ZZ_flag_freckles')


    # ########## [Forced unfolding] ##########
    def test_forced_unfolding(self):
        nyquist_velocity = 30
        dds_radd_eff_unamb_vel = 0
        center = 0
        forced_unfolding_mask = solo.forced_unfolding_masked(
            self.radar.fields['VV']['data'], nyquist_velocity, dds_radd_eff_unamb_vel, center)
        self.radar.add_field_like('VV', 'VV_forced_unfolding',
                            forced_unfolding_mask, replace_existing=True)
        self.graphPlot('VV_forced_unfolding')


    # ####### [Unfold First Good Gate] #######
    def test_unfold_first(self):
        nyquist_velocity = 25
        dds_radd_eff_unamb_vel = 5
        max_pos_folds = 10
        max_neg_folds = 10
        ngates_averaged = 20
        last_good_v0 = [1] * self.radar.ngates
        BB_unfolding_fgg_mask = solo.unfold_first_good_gate_masked(
            self.radar.fields['VV']['data'], nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
        self.radar.add_field_like('VV', 'VV_unfold_first_good_gate',
                            BB_unfolding_fgg_mask, replace_existing=True)
        self.graphPlot('VV_unfold_first_good_gate')


    # ######### [Unfold Local Wind] ##########
    def test_unfold_local(self):
        ew_wind = 5
        ns_wind = 5
        ud_wind = 5
        max_pos_folds = 10
        max_neg_folds = 10
        ngates_averaged = 20
        solo.unfold_local_wind_fields(self.radar, 'VV', 'VV_unfold_local_wind', ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged)
        self.graphPlot('VV_unfold_local_wind')

    ############ [Radial Shear] #############


    def test_radial_shear(self):
        seds_gate_diff_interval = round(self.radar.ngates / 2)
        radial_shear_mask = solo.radial_shear_masked(
            self.radar.fields['ZZ']['data'], seds_gate_diff_interval)
        self.radar.add_field_like('ZZ', 'ZZ_radial_shear',
                            radial_shear_mask, replace_existing=True)  # velocity
        self.graphPlot('ZZ_radial_shear')


    ############## [Rain Rate] ##############
    def test_rain_rate(self):
        # for any good values 'g', sets it to g = (1/300) * 10 ^ (0.1 * g * d_const)
        d_const = 6
        rain_rate_mask = solo.rain_rate_masked(self.radar.fields['VV']['data'], d_const)
        self.radar.add_field_like('VV', 'VV_rain_rate', rain_rate_mask,
                            replace_existing=True)
        self.graphPlot('VV_rain_rate')


path_to_file = Path.cwd() / Path('tests/data/radar_data_b.nc')

starttime = timeit.default_timer()
print("Starting...")
tp = TestPlots(path_to_file, 'reflectivity', 'velocity', False)
tp.test_despeckle()
print("Finished:", timeit.default_timer() - starttime)

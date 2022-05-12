import timeit
from pathlib import Path
import pyart
import matplotlib.pyplot as plt
import src.pysolo as solo


class TestPlots:

    def __init__(self, pathToData, reflectivity_field, velocity_field, showGraphs=False) -> None:
        self.radar: pyart.core.Radar = pyart.io.read(pathToData)
        self.reflectivity_field = reflectivity_field
        self.velocity_field = velocity_field
        try:
            self.display = pyart.graph.RadarMapDisplay(self.radar)
            self.graph = showGraphs
        except pyart.exceptions.MissingOptionalDependency:
            print("Cartopy is not installed. Skipping graphing...")
            self.graph = None
        print(list(self.radar.fields.keys()))
        print("Number of rays:", self.radar.nrays)
        print("Number of gates:", self.radar.ngates)

    def graphPlot(self, plot_field, file_path='outputs/quick-test.png'):
        if self.graph:
            print("Running plot grapher")
            _, ax = plt.subplots(ncols=2, figsize=(15, 7))
            self.display.plot(field=self.reflectivity_field, vmin=-40, vmax=40, title=self.reflectivity_field, cmap='pyart_NWSRef', ax=ax[0])
            self.display.set_limits((-50, 50), (-10, 35), ax=ax[0])
            self.display.plot(field=plot_field, vmin=-40, vmax=40, title=plot_field, cmap='pyart_NWSRef', ax=ax[1])
            self.display.set_limits((-50, 50), (-10, 35), ax=ax[1])
            plt.suptitle(plot_field, fontsize=16)
            # plt.show()
            plt.savefig(file_path)

    def demoThreshold(self, result_field):
        if self.graph:
            fig = plt.figure(figsize=(14, 14))
            ax = fig.add_subplot(221)
            self.display.plot(field=self.reflectivity_field, vmin=-10, vmax=30, title=f"Original ({self.reflectivity_field}) (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            ax = fig.add_subplot(222)
            self.display.plot(field=result_field, vmin=-10, vmax=30, title=f"{result_field} (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            ax = fig.add_subplot(223)
            self.display.plot(field=self.velocity_field, vmin=-10, vmax=30, title=f"Original ({self.velocity_field}) (PPI)", cmap='pyart_NWSRef')
            self.display.set_limits((-20, 20), (-5, 25), ax=ax)
            plt.show()

    ############ [Despeckle] ##############

    def test_despeckle(self):
        a_speckle = 2
        solo.despeckle_field(self.radar, self.reflectivity_field, f'{self.reflectivity_field}_despeckled', a_speckle)
        self.graphPlot(f'{self.reflectivity_field}_despeckled')

    # ############# [Ring Zap] ##############

    def test_ring_zap(self):
        from_km = 25
        to_km = 30

        solo.ring_zap_fields(self.radar, self.reflectivity_field, 'test_ring_zapped_1', from_km, to_km)
        self.graphPlot('test_ring_zapped_1', 'outputs/ringzap/ring-test-2.png')

    # ############ [Threshold] ##############

    def test_threshold(self):
        thr_1 = -1
        thr_2 = 0

        solo.threshold_fields(self.radar, self.reflectivity_field, self.velocity_field, 'test_threshold', solo.Where.BELOW, thr_1, thr_2)
        self.demoThreshold('test_threshold')

    # ########### [Merge Fields] #############

    def test_merge(self):
        solo.merge_fields_field(self.radar, self.reflectivity_field, self.velocity_field, 'test_merge')
        self.graphPlot('test_merge', 'outputs/merge/merge-test-2.png')

    # ############# [Deglitch] ##############

    def test_deglitch(self):
        deglitch_threshold = 1
        deglitch_radius = 20
        deglitch_min_bins = 27

        solo.flag_glitches_field(self.radar, self.reflectivity_field, 'test_flag_glitch', deglitch_threshold, deglitch_radius, deglitch_min_bins)
        self.graphPlot('test_flag_glitch', 'outputs/deglitch/deglitch-test-2.png')

    # ############## [Freckles] ##############

    def test_freckles(self):
        freckle_threshold = 12
        freckle_avg_count = 2

        solo.flag_freckles_field(self.radar, self.reflectivity_field, 'test_flag_freckles', freckle_threshold, freckle_avg_count)
        self.graphPlot('test_flag_freckles', 'outputs/freckles/freckles-test-2.png')

    # ########## [Forced unfolding] ##########

    def test_forced_unfolding(self):
        nyquist_velocity = 30
        dds_radd_eff_unamb_vel = 0
        center = 0

        solo.forced_unfolding_field(self.radar, self.velocity_field, 'test_forced_unfolding', nyquist_velocity, dds_radd_eff_unamb_vel, center)
        self.graphPlot('test_forced_unfolding', 'outputs/forced_unfolding/forced_unfolding-test-2.png')

    # ####### [Unfold First Good Gate] #######

    def test_unfold_first(self):
        dds_radd_eff_unamb_vel = 5
        max_pos_folds = 10
        max_neg_folds = 10
        ngates_averaged = 20
        last_good_v0 = [1] * self.radar.ngates
        BB_unfolding_fgg_mask = solo.unfold_first_good_gate_masked(self.radar.fields['VV']['data'], dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
        self.radar.add_field_like('VV', 'VV_unfold_first_good_gate', BB_unfolding_fgg_mask, replace_existing=True)
        self.graphPlot('VV_unfold_first_good_gate')

    # ######### [Unfold Local Wind] ##########

    def test_unfold_local(self):
        ew_wind = 5
        ns_wind = 5
        ud_wind = 5
        max_pos_folds = 10
        max_neg_folds = 10
        ngates_averaged = 20
        solo.unfold_local_wind_fields(self.radar, self.velocity_field, 'test_unfold_local_wind', ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged)
        self.graphPlot('test_unfold_local_wind')

    ############ [Radial Shear] #############

    def test_radial_shear(self):
        seds_gate_diff_interval = round(self.radar.ngates / 2)

        solo.radial_shear_field(self.radar, self.reflectivity_field, 'test_radial_shear', seds_gate_diff_interval)
        self.graphPlot('test_radial_shear', 'outputs/radial_shear/radial_shear-2.png')

    ############## [Rain Rate] ##############

    def test_rain_rate(self):
        d_const = 1

        solo.rain_rate_field(self.radar, self.velocity_field, 'test_rain_rate', d_const)
        self.graphPlot('test_rain_rate', 'outputs/rain_rate/rain_rate-2.png')

    def all(self):
        self.test_despeckle()
        self.test_ring_zap()
        self.test_threshold()
        self.test_merge()
        self.test_deglitch()
        self.test_freckles()
        self.test_forced_unfolding()
        self.test_unfold_local()
        self.test_radial_shear()
        self.test_rain_rate()


path_to_file = Path.cwd() / Path('tests/data/radar_data_b.nc')

starttime = timeit.default_timer()
print("Starting...")
tp = TestPlots(path_to_file, 'reflectivity', 'velocity', True)
tp.test_despeckle()
print("Finished:", timeit.default_timer() - starttime)

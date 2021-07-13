from numpy.ma.core import masked_equal
import pyart
import matplotlib.pyplot as plt
from copy import *
from pathlib import Path
import pysolo_package as solo
from datetime import datetime

def main():
    path_to_file = Path.cwd() / Path('tests/data/sgpxsaprsecI5.20180529.090013.nc')

    radar = pyart.io.read(path_to_file)

    print("Scan type:", radar.scan_type)
    max = radar.fields['velocity']['data'].max()
    min = radar.fields['velocity']['data'].min()
    print("min: %d, max: %d" % (min, max))
    print("nsweeps: %d, nrays: %d, ngates: %s" % (radar.nsweeps, radar.nrays, radar.ngates))
    print(radar.instrument_parameters.keys())

    # Radar fields:
    #
    # total_power
    # reflectivity
    # velocity
    # spectrum_width
    # differential_reflectivity
    # specific_differential_phase
    # cross_correlation_ratio
    # normalized_coherent_power
    # differential_phase
    # ground_clutter
    # sounding_temperature
    # height
    # signal_to_noise_ratio
    # velocity_texture
    # gate_id
    # simulated_velocity
    # corrected_velocity
    # unfolded_differential_phase
    # corrected_differential_phase
    # filtered_corrected_differential_phase
    # corrected_specific_diff_phase
    # filtered_corrected_specific_diff_phase
    # vulp_differential_phase
    # vulp_specific_diff_phase
    # mes_differential_phase_forwardmes_differential_phase_reversemes_specific_diff_phase


    display = pyart.graph.RadarMapDisplay(radar)

    def graphPlot(plot_field, ref):
        fig, ax = plt.subplots(ncols=2, figsize=(15,7))
        display.plot(field=ref, vmin=-15, vmax=15, title=ref, cmap='pyart_balance', ax=ax[0], sweep=1)
        display.plot(field=plot_field, vmin=-15, vmax=15, title=plot_field, cmap='pyart_balance', ax=ax[1], sweep=1)
        plt.suptitle(plot_field, fontsize=16)
        plt.show()

        plt_name = 'test_dealiasing_%s.png' % datetime.now().strftime(r"%d_%m_%Y_%H_%M_%S")
        dir = Path.cwd() / Path("tests/results/%s" % plt_name)
        plt.savefig(str(dir))

    ########## [Forced unfolding] ##########
    # Nyquist Velocity is the maximum velocity (in meters per second) that the radar can measure
    nyquist_velocity = radar.get_nyquist_vel(0) # 10.695 m/s
    # dds_radd_eff_unamb_vel is the maximum unambiguous range of the radar (in meters)
    dds_radd_eff_unamb_vel = radar.instrument_parameters['unambiguous_range']['data'].tolist()[0] # 108620.65 m
    center = 0
    forced_unfolding_mask = solo.forced_unfolding_masked(radar.fields['velocity']['data'], nyquist_velocity, dds_radd_eff_unamb_vel, center)

    missing = radar.fields['velocity']['data'].fill_value
    input_list = radar.fields['velocity']['data'].tolist(missing)
    output_list = forced_unfolding_mask.tolist(missing)

    changes = 0
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if (input_list[i][j] != output_list[i][j]):
                changes += 1
    print("Changes:", changes)

    radar.add_field_like('velocity', 'velocity_forced_unfolding', forced_unfolding_mask, replace_existing=True)

    graphPlot('velocity_forced_unfolding', 'velocity')

if __name__ == "__main__":
    main()

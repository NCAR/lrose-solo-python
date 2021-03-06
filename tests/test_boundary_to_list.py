from pathlib import Path
import pyart
import matplotlib.pyplot as plt
import src.pysolo as solo

DATA_FILE_DIR = "tests/data/subset_data/sweep1_VEL_F_max_range_30/cfrad.20150626_000730.199_to_20150626_000800.311_SPOL_SUR.nc"
BOUNDARY_FILE_DIR = "tests/data/subset_data/sweep1_VEL_F_max_range_30/fieldVEL_F-sweep1-Boundary1"
FIELD = "VEL_F"


def main():
    path_to_data_file = Path.cwd() / Path(DATA_FILE_DIR)
    path_to_boundary_file = Path.cwd() / Path(BOUNDARY_FILE_DIR)

    radar = pyart.io.read(path_to_data_file)

    boundary_list_of_lists = solo.get_boundary_mask(radar, path_to_boundary_file)

    display = pyart.graph.RadarMapDisplay(radar)

    from_km = 0
    to_km = 120
    kilometers_between_gates = radar.range['meters_between_gates'] / 1000
    ring_zapped_mask = solo.ring_zap_masked(radar.fields[FIELD]['data'], from_km, to_km, kilometers_between_gates, boundary_masks=boundary_list_of_lists)
    radar.add_field_like(FIELD, f'{FIELD}_ring_zapped', ring_zapped_mask, replace_existing=True)

    _, ax = plt.subplots(ncols=2, figsize=(15, 7))
    display.plot(field=FIELD, title=FIELD, cmap='pyart_NWSRef', ax=ax[0])
    display.plot(field=f'{FIELD}_ring_zapped', title=f'{FIELD}_ring_zapped', cmap='pyart_NWSRef', ax=ax[1])
    # display.set_limits(ylim=[-120, 0], xlim=[-100, 100], ax=ax[0])
    # display.set_limits(ylim=[-120, 0], xlim=[-100, 100], ax=ax[1])
    plt.suptitle(FIELD, fontsize=16)
    plt.savefig('quick-test.png')


if __name__ == "__main__":
    main()
    print("end")

# https://github.com/NCAR/lrose-HawkEdit/tree/main/test_cases/touch_up_editing/data/pecan

# this module handles mapping of C-function names
# also handles which library to import based on platform

from pathlib import Path
import ctypes
import struct
from src.pysolo.c_wrapper.function_alias import aliases
from src.pysolo.solo_functions.solo_despeckle import despeckle_masked, despeckle
import numpy as np
from statistics import mean
import pyart


data_file_dir = "tests/data/cfrad.20150626_000730.199_to_20150626_001312.085_SPOL_PunSur_SUR.nc"
boundary_file_dir = "tests/data/fieldDBZ_F-sweep1-Boundary1"


def list_to_array(data_list, type_c):
    """ convert Python list to ctypes array """
    if data_list is None:
        return None
    data_length = type_c * len(data_list)
    return ctypes.cast(data_length(*data_list), ctypes.POINTER(type_c))


def array_to_list(input_array, size):
    """ converts ctypes array to Python list """
    return [input_array[i] for i in range(size)]


def parse_boundary_file():
    """ extracts two lists, for x and y points, of boundary file """
    path_to_boundary_file = Path.cwd() / Path(boundary_file_dir)

    data = path_to_boundary_file.read_bytes()
    iterations = int((len(data) - 20) / 8)

    i = int.from_bytes(data[:5], byteorder="little", signed=True)
    ints = struct.unpack("iiffif", data[:24])
    print("header", ints)

    print("\n{:<8} {:<8} {:<8} {:<8} {:<8}".format(
        "i", "start", "end", "x", "y"))

    x_points = []
    y_points = []

    for i in range(iterations):
        start = 20 + i * 8
        end = start + 8
        x, y = struct.unpack("ff", data[start:end])
        x_points.append(int(x))
        y_points.append(int(y))
        print("{:<8} {:<8} {:<8} {:<8} {:<8}".format(i, start, end, x, y))

    print()
    return x_points, y_points


def main():
    path_to_data_file = Path.cwd() / Path(data_file_dir)
    radar = pyart.io.read(path_to_data_file)

    x_points, y_points = parse_boundary_file()

    # boundary mask function returns void
    aliases["get_boundary_mask"].restype = None

    # define the boundary mask function's argument types
    aliases["get_boundary_mask"].argtypes = (
        ctypes.POINTER(ctypes.c_long),
        ctypes.POINTER(ctypes.c_long),
        ctypes.c_int,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_int,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.POINTER(ctypes.c_bool),
    )

    radar_latitude_list = radar.latitude['data'].tolist()
    radar_longitude_list = radar.longitude['data'].tolist()
    radar_altitude_list = radar.altitude['data'].tolist()
    radar_azimuth_list = radar.azimuth['data'].tolist()

    radar_tilt_list = [0] * radar.ngates if radar.tilt is None else radar.tilt['data'].tolist()
    radar_rotation_list = [0] * radar.ngates if radar.rotation is None else radar.rotation['data'].tolist()

    #  =====Scan modes=====
    # define              CAL 0
    # define              PPI 1
    # define              COP 2
    # define              RHI 3
    # define              VER 4
    # define              TAR 5
    # define              MAN 6
    # define              IDL 7
    # define              SUR 8
    # define              AIR 9
    # define              HOR 10

    #  ====Radar types=====
    # define           GROUND 0
    # define         AIR_FORE 1
    # define          AIR_AFT 2
    # define         AIR_TAIL 3
    # define           AIR_LF 4
    # define             SHIP 5
    # define         AIR_NOSE 6
    # define        SATELLITE 7
    # define     LIDAR_MOVING 8
    # define      LIDAR_FIXED 9

    radar_scan_mode = 1  # default to PPI
    radar_scan_type = 0  # default to GROUND

    if radar.scan_type == 'rhi':
        radar_scan_mode = 3

    if radar.metadata['platform_type'] == 'aircraft_tail':
        radar_scan_type = 3

    boundary_list_of_lists = []

    print("="*30)
    print(f"ngates: {radar.ngates}")
    print(f"latitude list size: {len(radar_latitude_list)}")
    print(f"longitude list size: {len(radar_longitude_list)}")
    print(f"altitude list size: {len(radar_altitude_list)}")
    print(f"azimuth list size: {len(radar_azimuth_list)}")
    print(f"tilt list size: {len(radar_tilt_list)}")
    print(f"rotation list size: {len(radar_rotation_list)}")
    print("="*30)

    for i in range(radar.nrays):

        boundary = list_to_array([], ctypes.c_bool)

        aliases["get_boundary_mask"](
            list_to_array(x_points, ctypes.c_long),  # x_points
            list_to_array(y_points, ctypes.c_long),  # y_points
            ctypes.c_int(len(x_points)),  # npoints
            # next 3 parameters have length 1 for a particular set of data
            ctypes.c_float(radar_latitude_list[0]),  # radar_origin_latitude
            ctypes.c_float(radar_longitude_list[0]),  # radar_origin_longitude
            ctypes.c_float(radar_altitude_list[0]),  # radar_origin_altitude
            ctypes.c_float(0),  # boundary_origin_tilt
            ctypes.c_float(0),  # boundary_origin_latitude
            ctypes.c_float(0),  # boundary_origin_longitude
            ctypes.c_float(0),  # boundary_origin_altitude
            ctypes.c_int(radar.ngates),  # nGates
            ctypes.c_float(radar.range['meters_between_gates']),  # gateSize
            # distanceToCellInMeters
            ctypes.c_float(radar.range['meters_to_center_of_first_gate']),
            ctypes.c_float(radar_azimuth_list[i]),  # azimuth
            ctypes.c_int(radar_scan_mode),  # radar_scan_mode
            ctypes.c_int(radar_scan_type),  # radar_type
            ctypes.c_float(radar_tilt_list[i]),  # tilt_angle
            ctypes.c_float(radar_rotation_list[i]),  # rotation_angle
            boundary,  # boundary_mask_out
        )

        boundary_list_of_lists.append(boundary)

    # https://github.com/NCAR/lrose-HawkEdit/tree/main/test_cases/touch_up_editing/data/pecan


if __name__ == "__main__":
    main()

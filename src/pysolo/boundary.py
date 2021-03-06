from pathlib import Path
import struct
import ctypes
from typing import List
import pyart
from .c_wrapper.function_alias import aliases
from .c_wrapper.conversions import list_to_array, array_to_list


def parse_boundary_file(boundary_path: str):
    """ extracts two lists, for x and y points, of boundary file """
    path_to_boundary_file = Path(boundary_path)

    data = path_to_boundary_file.read_bytes()
    iterations = int((len(data) - 20) / 8)

    i = int.from_bytes(data[:5], byteorder="little", signed=True)
    # print("header", ints)

    # print("\n{:<8} {:<8} {:<8} {:<8} {:<8}".format(
    #     "i", "start", "end", "x", "y"))

    x_points = []
    y_points = []

    for i in range(iterations):
        start = 20 + i * 8
        end = start + 8
        x, y = struct.unpack("ff", data[start:end])
        x_points.append(int(x))
        y_points.append(int(y))
        # print("{:<8} {:<8} {:<8} {:<8} {:<8}".format(i, start, end, x, y))

    # print()
    return x_points, y_points


def get_boundary_mask(radar: pyart.core.Radar, boundary_path: str) -> List[List[bool]]:

    x_points, y_points = parse_boundary_file(boundary_path)

    # boundary mask function returns void
    # Source code
    # https://github.com/NCAR/lrose-core/blob/adfcb5e0368f7e8bbf37f107fee70be50a64fed3/codebase/libs/Solo/src/Solo/Boundary.cc#L21
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

    # extract these lists from the radar's data
    radar_azimuth_list = radar.azimuth['data'].tolist()

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
    elif radar.metadata['platform_type'] == 'fixed':
        radar_scan_type = 9

    boundary_list_of_lists = []


    for i in range(radar.nrays):
        boundary = list_to_array([True] * radar.ngates, ctypes.c_bool)
        x_array = list_to_array(x_points, ctypes.c_long)
        y_array = list_to_array(y_points, ctypes.c_long)

        aliases["get_boundary_mask"](
            x_array,  # x_points
            y_array,  # y_points
            ctypes.c_int(len(x_points)),  # npoints

            ctypes.c_float(radar.latitude['data'].tolist()[0]),  # radar_origin_latitude
            ctypes.c_float(radar.longitude['data'].tolist()[0]),  # radar_origin_longitude
            ctypes.c_float(radar.altitude['data'].tolist()[0]),  # radar_origin_altitude

            ctypes.c_float(0),  # boundary_origin_tilt
            ctypes.c_float(radar.latitude['data'].tolist()[0]),  # boundary_origin_latitude
            ctypes.c_float(radar.longitude['data'].tolist()[0]),  # boundary_origin_longitude
            ctypes.c_float(radar.altitude['data'].tolist()[0]),  # boundary_origin_altitude

            ctypes.c_int(radar.ngates),  # nGates
            ctypes.c_float(radar.range['meters_between_gates'] / 1000),  # gateSize
            ctypes.c_float(radar.range['meters_to_center_of_first_gate'] / 1000),  # distanceToCellInMeters
            ctypes.c_float(radar_azimuth_list[i]),  # azimuth
            ctypes.c_int(radar_scan_mode),  # radar_scan_mode
            ctypes.c_int(radar_scan_type),  # radar_type
            ctypes.c_float(0),  # tilt_angle
            ctypes.c_float(0),  # rotation_angle ----- not used by code
            boundary  # boundary_mask_out
        )

        boundary_list_of_lists.append(array_to_list(boundary, radar.ngates))

    return boundary_list_of_lists

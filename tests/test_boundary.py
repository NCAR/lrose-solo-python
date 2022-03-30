import ctypes
from src.pysolo.c_wrapper.function_alias import aliases
from src.pysolo.c_wrapper.conversions import list_to_array, array_to_list

PPI = 1
GROUND = 0

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

def test_boundary_one():
    nBoundaryPoints = 4

    x_points = [2, 13, 13, 2]
    y_points = [2, 2, 11, 11]

    gateSize = 1.5
    nGates = 15
    distanceToCellNInMeters = 3
    azimuth = 45.0
    radar_scan_mode = PPI
    radar_type = GROUND

    radar_origin_latitude = 40.0
    radar_origin_longitude = 40.0
    radar_origin_altitude = 0.0

    boundary_origin_latitude = 40.0
    boundary_origin_longitude = 40.0
    boundary_origin_altitude = 0.0


    boundary = list_to_array([True] * nGates, ctypes.c_bool)

    aliases["get_boundary_mask"](
        list_to_array(x_points, ctypes.c_long),  # x_points
        list_to_array(y_points, ctypes.c_long),  # y_points
        nBoundaryPoints,  # npoints

        ctypes.c_float(radar_origin_latitude),  # radar_origin_latitude
        ctypes.c_float(radar_origin_longitude),  # radar_origin_longitude
        ctypes.c_float(radar_origin_altitude),  # radar_origin_altitude

        ctypes.c_float(0),  # boundary_origin_tilt
        ctypes.c_float(boundary_origin_latitude),  # boundary_origin_latitude
        ctypes.c_float(boundary_origin_longitude),  # boundary_origin_longitude
        ctypes.c_float(boundary_origin_altitude),  # boundary_origin_altitude

        ctypes.c_int(nGates),  # nGates
        ctypes.c_float(gateSize),  # gateSize
        ctypes.c_float(distanceToCellNInMeters),  # distanceToCellInMeters
        ctypes.c_float(azimuth),  # azimuth
        ctypes.c_int(radar_scan_mode),  # radar_scan_mode
        ctypes.c_int(radar_type),  # radar_type
        ctypes.c_float(0),  # tilt_angle
        ctypes.c_float(0),  # rotation_angle ----- not used by code
        boundary  # boundary_mask_out
    )

    assert array_to_list(boundary, nGates) == [True, True, True, True, True, True, True, True, True, False, False, False, False, False, False]


def test_boundary_two():
    nBoundaryPoints = 4

    x_points = [2, 13, 13, 2]
    y_points = [2, 2, 11, 11]

    gateSize = 1.5
    nGates = 15
    distanceToCellNInMeters = 0
    azimuth = 45.0
    radar_scan_mode = PPI
    radar_type = GROUND

    radar_origin_latitude = 40.0
    radar_origin_longitude = 40.0
    radar_origin_altitude = 0.0

    boundary_origin_latitude = 40.0
    boundary_origin_longitude = 40.0
    boundary_origin_altitude = 0.0


    boundary = list_to_array([True] * nGates, ctypes.c_bool)

    aliases["get_boundary_mask"](
        list_to_array(x_points, ctypes.c_long),  # x_points
        list_to_array(y_points, ctypes.c_long),  # y_points
        nBoundaryPoints,  # npoints

        ctypes.c_float(radar_origin_latitude),  # radar_origin_latitude
        ctypes.c_float(radar_origin_longitude),  # radar_origin_longitude
        ctypes.c_float(radar_origin_altitude),  # radar_origin_altitude

        ctypes.c_float(0),  # boundary_origin_tilt
        ctypes.c_float(boundary_origin_latitude),  # boundary_origin_latitude
        ctypes.c_float(boundary_origin_longitude),  # boundary_origin_longitude
        ctypes.c_float(boundary_origin_altitude),  # boundary_origin_altitude

        ctypes.c_int(nGates),  # nGates
        ctypes.c_float(gateSize),  # gateSize
        ctypes.c_float(distanceToCellNInMeters),  # distanceToCellInMeters
        ctypes.c_float(azimuth),  # azimuth
        ctypes.c_int(radar_scan_mode),  # radar_scan_mode
        ctypes.c_int(radar_type),  # radar_type
        ctypes.c_float(0),  # tilt_angle
        ctypes.c_float(0),  # rotation_angle ----- not used by code
        boundary  # boundary_mask_out
    )

    assert array_to_list(boundary, nGates) == [False, True, True, True, True, True, True, True, True, True, True, False, False, False, False]

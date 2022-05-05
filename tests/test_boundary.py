import src.pysolo as solo

PPI = 1
GROUND = 0

class TestBoundary():

    def test_boundary_one(self):
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

        boundary = [True] * nGates

        output = solo.boundary.run_boundary_on_ray(x_points, y_points, nBoundaryPoints, radar_origin_latitude, radar_origin_longitude, radar_origin_altitude,
            boundary_origin_latitude, boundary_origin_longitude, boundary_origin_altitude, nGates, gateSize, distanceToCellNInMeters, azimuth, radar_scan_mode, radar_type, boundary)

        assert output == [True, True, True, True, True, True, True, True, True, False, False, False, False, False, False]


    def test_boundary_two(self):
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

        boundary = [True] * nGates

        output = solo.boundary.run_boundary_on_ray(x_points, y_points, nBoundaryPoints, radar_origin_latitude, radar_origin_longitude, radar_origin_altitude,
            boundary_origin_latitude, boundary_origin_longitude, boundary_origin_altitude, nGates, gateSize, distanceToCellNInMeters, azimuth, radar_scan_mode, radar_type, boundary)

        assert output == [False, True, True, True, True, True, True, True, True, True, True, False, False, False, False]

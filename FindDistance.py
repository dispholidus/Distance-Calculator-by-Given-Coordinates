import math


class FindDistance:
    WORLD_RADIUS = 6371

    @staticmethod
    def find_latitude(x, line):
        y = ((x - line[0]) * (line[1] - line[3]) / (line[0] - line[2])) + line[1]
        return y

    @staticmethod
    def haversine_algorithm(point0, point1):
        x1 = point0[0] * math.pi / 180
        x2 = point1[0] * math.pi / 180
        deltaX = (point1[0] - point0[0]) * math.pi / 180
        deltaY = (point1[1] - point0[1]) * math.pi / 180

        a = math.sin(deltaX / 2) * math.sin(deltaX / 2) + math.cos(x1) * math.cos(x2) * math.sin(deltaY / 2) * math.sin(
            deltaY / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = FindDistance.WORLD_RADIUS * 1000 * c
        return distance

    @staticmethod
    def calc_longtitude_distance(latitude):
        longtitude_distance = 2 * math.pi * FindDistance.WORLD_RADIUS * math.cos(math.radians(latitude)) / 360
        return longtitude_distance

    @staticmethod
    def meter_to_degree(distance, frequency):
        degree = frequency / distance
        return degree

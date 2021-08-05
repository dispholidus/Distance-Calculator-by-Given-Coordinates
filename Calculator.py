import math


class Calculator:
    WORLD_RADIUS = 6371

    @staticmethod
    def find_latitude(x, line0, line1):
        y = ((x - line0[0]) * (line0[1] - line1[1]) / (line0[0] - line1[0])) + line0[1]
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

        distance = Calculator.WORLD_RADIUS * 1000 * c
        return distance/1000

    @staticmethod
    def calc_longtitude_distance(latitude):
        longtitude_distance = 2 * math.pi * Calculator.WORLD_RADIUS * math.cos(math.radians(latitude)) / 360
        return longtitude_distance

    @staticmethod
    def meter_to_degree(longtitude_distance, distance):
        degree = distance / longtitude_distance
        return degree

    @staticmethod
    def find_x_distance(point0, point1, frequency):
        # Burayı sıfırdan yaz
        radian = math.atan(((point1[1] - point0[1]) * 111) / ((point1[0] - point0[0]) * Calculator.calc_longtitude_distance(point0[1])))
        x_distance = math.sqrt((frequency * frequency) - (math.tan(radian) * math.tan(radian)) - 1)
        return x_distance

import math


class Calculator:
    WORLD_RADIUS = 6371

    @staticmethod
    def haversine_algorithm(point0, point1):
        y1 = math.radians(point0[1])
        y2 = math.radians(point1[1])
        deltaY = (point1[1] - point0[1]) * math.pi / 180
        deltaX = (point1[0] - point0[0]) * math.pi / 180

        a = math.sin(deltaY / 2) * math.sin(deltaY / 2) + math.cos(y1) * math.cos(y2) * math.sin(deltaX / 2) * math.sin(
            deltaX / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = Calculator.WORLD_RADIUS * c

        return distance

    @staticmethod
    def calculate_bearing(point0, point1):
        y1 = math.radians(point0[1])
        y2 = math.radians(point1[1])
        x1 = math.radians(point0[0])
        x2 = math.radians(point1[0])

        a = math.sin(x2 - x1) * math.cos(y2)
        b = math.cos(y1) * math.sin(y2) - math.sin(y1) * math.cos(y2) * math.cos(x2 - x1)
        radian_brng = math.atan2(a, b)

        return math.degrees(radian_brng)

    @staticmethod
    def find_second_point(point, bearing, distance):
        second_point = [0, 0]
        x = math.radians(point[0])
        y = math.radians(point[1])
        bearing = math.radians(bearing)
        angular_distance = distance / Calculator.WORLD_RADIUS

        siny1 = math.sin(y) * math.cos(angular_distance) + math.cos(y) * math.sin(angular_distance) * math.cos(bearing)
        y1 = math.asin(siny1)
        b = math.sin(bearing) * math.sin(angular_distance) * math.cos(y)
        a = math.cos(angular_distance) - math.sin(y) * siny1
        x1 = x + math.atan2(b, a)

        second_point[0] = math.degrees(x1)
        second_point[1] = math.degrees(y1)

        return second_point

    @staticmethod
    def cross_track_distance(startPoint, endPoint, checkpoint):

        startToCheckpointD = Calculator.haversine_algorithm(startPoint, checkpoint) / Calculator.WORLD_RADIUS
        startToCheckpointB = math.radians(Calculator.calculate_bearing(startPoint, checkpoint))
        startToEndB = math.radians(Calculator.calculate_bearing(startPoint, endPoint))

        distance = abs(math.asin(math.sin(startToCheckpointD) * math.sin(startToCheckpointB - startToEndB)))

        return distance * Calculator.WORLD_RADIUS*1000

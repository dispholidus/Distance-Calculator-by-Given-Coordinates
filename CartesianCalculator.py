import math


class CartesianCalculator:
    WORLD_RADIUS = 6371

    @staticmethod
    def calculate_distance(point0, point1):
        longtitude_distance = (math.cos(point0[1]) * CartesianCalculator.WORLD_RADIUS) / 360
        distance = math.sqrt(math.pow((point1[0] - point0[0]) * longtitude_distance, 2) + (math.pow((point1[1] - point0[1]) * 111, 2)))

        return distance

    @staticmethod
    def find_second_point(point0, point1, distance):
        longtitude_distance = (abs((2 * math.pi * CartesianCalculator.WORLD_RADIUS) * math.cos(math.radians(point0[1]))) / 360)
        secondPoint = []
        tanAlfa = ((point1[1] - point0[1]) * 111) / ((point1[0] - point0[0]) * longtitude_distance)
        secondPointX = math.sqrt(math.pow(distance, 2) / ((math.pow(tanAlfa, 2) + 1) * math.pow(longtitude_distance, 2)))
        secondPointY = secondPointX * longtitude_distance * tanAlfa/111
        secondPoint.append(point0[0] + secondPointX)
        secondPoint.append(point0[1] + secondPointY)

        return secondPoint

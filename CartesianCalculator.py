import math


class CartesianCalculator:
    WORLD_RADIUS = 6371

    @staticmethod
    def calculate_distance(point0, point1):
        longtitude_distance = (math.cos(point0[1]) * 2 * math.pi * CartesianCalculator.WORLD_RADIUS) / 360
        distance = math.sqrt(math.pow((point1[0] - point0[0]) * longtitude_distance, 2) + (math.pow((point1[1] - point0[1]) * 111, 2)))

        return distance

    @staticmethod
    def find_checkpoint(point0, point1, distance):
        longtitude_distance = ((2 * math.pi * CartesianCalculator.WORLD_RADIUS) * math.cos(math.radians(point0[1]))) / 360
        checkpoint = []
        tanAlfa = ((point1[1] - point0[1]) * 111) / ((point1[0] - point0[0]) * longtitude_distance)
        checkpointX = math.sqrt(math.pow(distance, 2) / ((math.pow(tanAlfa, 2) + 1) * math.pow(longtitude_distance, 2)))
        checkpointY = checkpointX * longtitude_distance * tanAlfa/111
        checkpoint.append(point0[0] + checkpointX)
        checkpoint.append(point0[1] + checkpointY)

        return checkpoint

    @staticmethod
    def calculate_inclination(point0, point1):
        longtitude_distance = ((2 * math.pi * CartesianCalculator.WORLD_RADIUS) * math.cos(
            math.radians(point0[1]))) / 360
        inclination = (point1[1] - point0[1]) * 111 / (point1[0] - point0[0]) * longtitude_distance

        return inclination

    @staticmethod
    def find_second_point(point00, checkpoint, point10, point11):
        secondPoint = []
        longtitude_distance = ((2 * math.pi * CartesianCalculator.WORLD_RADIUS) * math.cos(
            math.radians(point00[1]))) / 360
        inclination0 = CartesianCalculator.calculate_inclination(point00, checkpoint)
        inclination1 = CartesianCalculator.calculate_inclination(point10, point11)
        inclination2 = -1/inclination0

        a = inclination2 * longtitude_distance
        b = inclination1 * longtitude_distance

        x = (a * checkpoint[0] - b * point10[0] + 111 * (point10[1] - checkpoint[1])) / (a-b)
        y = (b * (x-point10[0]) + point10[1] * 111) / 111

        secondPoint.append(x)
        secondPoint.append(y)

        return secondPoint

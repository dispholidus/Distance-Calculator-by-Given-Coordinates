from Calculator import *


class LineSegment:
    startPoint = []
    endPoint = []

    def __init__(self, startPoint, endPoint):
        self.startPoint = (startPoint[0], startPoint[1])
        self.endPoint = (endPoint[0], endPoint[1])
        self.length = Calculator.haversine_algorithm(startPoint, endPoint)
        self.bearing = Calculator.calculate_bearing(startPoint, endPoint)
        self.checkpoints = []

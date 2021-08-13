from Calculator import Calculator as calc


class LineSegment:
    startPoint = []
    endPoint = []

    def __init__(self, startPoint, endPoint):
        self.startPoint = (startPoint[0], startPoint[1])
        self.endPoint = (endPoint[0], endPoint[1])
        self.length = calc.haversine_algorithm(startPoint, endPoint)
        self.bearing = calc.calculate_bearing(startPoint, endPoint)
        self.checkpoints = []
        self.perpendicularSegment = []
        self.counterpartSegments = []


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
    def findcheckpoint(point, bearing, distance):
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

        return distance * Calculator.WORLD_RADIUS * 1000

    @staticmethod
    def find_perpendicular_points(lineSegment):
        rotatedSegments = []
        longtitude_distance = ((2 * math.pi * Calculator.WORLD_RADIUS) * math.cos(
            math.radians(lineSegment.startPoint[1]))) / 360
        for cp in lineSegment.checkpoints:
            tempPoint = Calculator.findcheckpoint(cp, lineSegment.bearing, 1)
            x = abs(tempPoint[0] - cp[0]) * longtitude_distance
            y = abs(tempPoint[1] - cp[1]) * 111
            rotatedby90 = [cp[0] + y / longtitude_distance, cp[1] - x / 111]
            rotatedby270 = [cp[0] - y / longtitude_distance, cp[1] + x / 111]

            rotatedSegments.append([rotatedby270, rotatedby90])

        return rotatedSegments


class IntersectionControl:

    @staticmethod
    def onSegment(p, q, r):
        if ((q.x <= max(p[0], r[0])) and (q.x >= min(p[0], r[0])) and
                (q[1] <= max([1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if val > 0:

            return 1
        elif val < 0:

            return 2
        else:

            return 0

    @staticmethod
    def doIntersect(mainSegment, secondSegment):
        longtitude_distance = ((2 * math.pi * Calculator.WORLD_RADIUS) * math.cos(
            math.radians(mainSegment.startPoint[1]))) / 360
        p1 = (mainSegment.startPoint[0] * longtitude_distance, mainSegment.startPoint[1] * 111)
        q1 = (mainSegment.endPoint[0] * longtitude_distance, mainSegment.endPoint[1] * 111)
        p2 = (secondSegment.startPoint[0] * longtitude_distance, secondSegment.startPoint[1] * 111)
        q2 = (secondSegment.endPoint[0] * longtitude_distance, secondSegment.endPoint[1] * 111)

        o1 = IntersectionControl.orientation(p1, q1, p2)
        o2 = IntersectionControl.orientation(p1, q1, q2)
        o3 = IntersectionControl.orientation(p2, q2, p1)
        o4 = IntersectionControl.orientation(p2, q2, q1)

        if (o1 != o2) and (o3 != o4):
            return True

        if (o1 == 0) and IntersectionControl.onSegment(p1, p2, q1):
            return True

        if (o2 == 0) and IntersectionControl.onSegment(p1, q2, q1):
            return True

        if (o3 == 0) and IntersectionControl.onSegment(p2, p1, q2):
            return True

        if (o4 == 0) and IntersectionControl.onSegment(p2, q1, q2):
            return True

        return False

    @staticmethod
    def findIntersectionPoint(segment1, segment2):
        y1 = math.radians(segment1.startPoint[1])
        x1 = math.radians(segment1.startPoint[0])
        y2 = math.radians(segment2.startPoint[1])
        x2 = math.radians(segment2.startPoint[0])
        brng1 = math.radians(segment1.bearing)
        brng2 = math.radians(segment2.bearing)
        deltaY = y2 - y1
        deltaX = x2 - x1

        angularDistance = 2 * math.asin(math.sqrt(math.sin(deltaY / 2) * math.sin(deltaY / 2) + math.cos(y1) * math.cos(y2) * math.sin(deltaX / 2) * math.sin(deltaX / 2)))

        cosTetaA = (math.sin(y2) - math.sin(y1) * math.cos(angularDistance)) / (math.sin(angularDistance) * math.cos(y1))
        cosTetaB = (math.sin(y1) - math.sin(y2) * math.cos(angularDistance)) / (math.sin(angularDistance) * math.cos(y2))
        tetaA = math.acos(min(max(cosTetaA, -1), 1))
        tetaB = math.acos(min(max(cosTetaB, -1), 1))

        if math.sin(x2 - x1) > 0:
            teta12 = tetaA
            teta21 = 2 * math.pi - tetaB
        elif math.sin(x2-x1) < 0:
            teta12 = 2 * math.pi - tetaA
            teta21 = tetaB

        alfa1 = brng1 - teta12
        alfa2 = teta21 - brng2

        cosAlfa3 = -math.cos(alfa1) * math.cos(alfa2) + math.sin(alfa1) * math.sin(alfa2) * math.cos(angularDistance)

        deltaY13 = math.atan2(math.sin(angularDistance) * math.sin(alfa1) * math.sin(alfa2), math.cos(alfa2) + math.cos(alfa1) * cosAlfa3)
        y3 = math.asin(min(max(math.sin(y1) * math.cos(deltaY13) + math.cos(y1) * math.sin(deltaY13) * math.cos(brng1), -1), 1))

        deltaX13 = math.atan2(math.sin(brng1) * math.sin(deltaY13) * math.cos(y1), math.cos(deltaY13) - math.sin(y1) * math.sin(y3))
        x3 = x1 + deltaX13

        intersectionPoint = [math.degrees(x3), math.degrees(y3)]

        return intersectionPoint

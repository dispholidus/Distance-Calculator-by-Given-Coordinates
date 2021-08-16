from os import path

from ReadKml import *
from Calculator import *
from TypeConverter import *
from LineSegment import LineSegment


class Main:
    distance = 0
    floatList0 = []
    floatList1 = []
    kml_files = []
    roots = []
    coordinateList = []
    segmentList = []
    checkpoints = []

    def __init__(self):
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR KUZEY.kml"))
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR GUNEY(1).kml"))

    def main(self):
        # kml dosyalarının içine xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" eklemeyi unutma
        # kml dosyalarının kordinat kısmında ki tüm boşlukları sil

        for k in self.kml_files:
            self.roots.append(ReadKml.read(k))
        for r in self.roots:
            self.coordinateList.append(TypeConverter.stringListtoFloatList(
                str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))
        for c in self.coordinateList:
            tempList = []
            for index, elem in enumerate(c):
                if index + 1 < len(c):
                    thisElem = c[index]
                    nextElem = c[index + 1]
                    obj = LineSegment(thisElem, nextElem)
                    tempList.append(obj)
            self.segmentList.append(tempList)
        for c in self.segmentList:
            self.checkpoints.append(self.find_checkpoints(c))
        for ls in self.segmentList:
            for p in ls:
                self.find_perpendicularSegments(p)
        for ls in self.segmentList:
            self.find_counterpartSegments(ls, self.segmentList)
        

    @staticmethod
    def find_checkpoints(coordinates):
        temp_list = []
        checkpoint_distance = 1
        j = 0
        checkpoint = coordinates[0].startPoint
        while j < len(coordinates):
            if Calculator.haversine_algorithm(checkpoint, coordinates[j].endPoint) >= checkpoint_distance:
                checkpoint = Calculator.findcheckpoint(checkpoint,
                                                       Calculator.calculate_bearing(checkpoint,
                                                                                    coordinates[j].endPoint),
                                                       checkpoint_distance)
                checkpoint_distance = 1
                coordinates[j].checkpoints.append(checkpoint)
                temp_list.append(checkpoint)
            else:
                checkpoint_distance = checkpoint_distance - Calculator.haversine_algorithm(checkpoint,
                                                                                           coordinates[j].endPoint)
                checkpoint = coordinates[j].endPoint
                j = j + 1
        return temp_list

    @staticmethod
    def find_perpendicularSegments(lineSegment):
        pointsList = Calculator.find_perpendicular_points(lineSegment)
        tempList = []
        for pl in pointsList:
            tempList.append(LineSegment(pl[0], pl[1]))
        lineSegment.perpendicularSegment = tempList

    @staticmethod
    def find_counterpartSegments(mainLine, segmentList):
        for i in segmentList:
            for j in mainLine:
                if i[0].startPoint != j.startPoint:
                    tempList = []
                    for k in j.perpendicularSegment:

                        for segment in i:
                            if IntersectionControl.doIntersect(k, segment):
                                tempList.append(segment)
                                break
                    j.counterpartSegments.append(tempList)
                else:
                    break


if __name__ == "__main__":
    Main().main()

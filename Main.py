from os import path

from ReadKml import *
from Calculator import *
from TypeConverter import *
from LineSegment import LineSegment
import pandas as pd


class Main:
    distance = 0
    floatList0 = []
    floatList1 = []
    kml_files = []
    roots = []
    coordinateList = []
    segmentList = []
    checkpoints = []
    counterPoints = []
    lineNames = []

    def __init__(self):
        self.kml_files.append(path.join("input/Hat_380kV_GELIBOLU 380 - UNIMAR KUZEY.kml"))
        self.kml_files.append(path.join("input/Hat_380kV_GELIBOLU 380 - UNIMAR GUNEY(1).kml"))
        self.kml_files.append(path.join("input/Hat_380kV_CORLU 380-HADIMKOY GIS(1).kml"))
        self.kml_files.append(path.join("input/Hat_380kV_CORLU 380-HADIMKOY GIS.kml"))
        self.kml_files.append(path.join("input/Hat_380kV_UNIMAR - HABIBLER(1).kml"))
        self.kml_files.append(path.join("input/Hat_380kV_UNIMAR - HABIBLER.kml"))
        self.kml_files.append(path.join("input/Hat_380kV_UNIMAR - IKITELLI(1).kml"))
        self.kml_files.append(path.join("input/Hat_380kV_UNIMAR - IKITELLI.kml"))

    def main(self):
        # kml dosyalarının içine xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" eklemeyi unutma
        # kml dosyalarının kordinat kısmında ki tüm boşlukları sil

        for k in self.kml_files:
            self.roots.append(ReadKml.read(k))
        for r in self.roots:
            lineName = str(r.Document.name)
            lineName = lineName.replace(".kml", "").replace("Hat", "").replace("-", " ").replace("_", "").replace(
                "380kV", "").replace("   ", " ")
            self.lineNames.append(lineName)
        for r in self.roots:
            self.coordinateList.append(TypeConverter.stringListtoFloatList(
                str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))
        for c in self.coordinateList:
            tempList = []
            for index, elem in enumerate(c):
                if index + 1 < len(c):
                    thisElem = elem
                    nextElem = c[index + 1]
                    obj = LineSegment(thisElem, nextElem)
                    tempList.append(obj)
            self.segmentList.append(tempList)
        for c in self.segmentList:
            self.checkpoints.append(self.find_checkpoints(c))
        self.calculate(1)

    def calculate(self, index):
        line = self.segmentList[index]
        lineName = str(self.roots[index].Document.name)
        lineName = lineName.replace(".kml", "").replace("Hat", "").replace("-", " ").replace("_", "").replace(
            "380kV", "").replace("   ", " ")
        self.lineNames.append(lineName)
        for p in line:
            self.find_perpendicularSegments(p)
        self.find_counterpartSegments(line, self.segmentList)
        self.find_distances(line, index)

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
                        isFilled = False
                        for segment in i:
                            if IntersectionControl.doIntersect(k, segment):
                                isFilled = True
                                tempList.append(segment)
                                break
                        if not isFilled:
                            tempList.append(0)
                    j.counterpartSegments.append(tempList)
                else:
                    break

    def find_distances(self, mainLine, index):
        distance_dict = {}
        counterpoint_dict = {}
        counter = 0
        for ind, elem in enumerate(self.lineNames):
            if ind != index:
                distance_dict[elem] = []
                counterpoint_dict[counter] = []
                counter = counter + 1
        for segment in mainLine:
            for cpsIndex, cps in enumerate(segment.counterpartSegments):
                for spIndex, elem in enumerate(segment.perpendicularSegment):
                    if len(cps) != 0:
                        if cps[spIndex] == 0:
                            counterpoint_dict[cpsIndex].append(0)
                        else:
                            if IntersectionControl.orientation(segment.startPoint, segment.checkpoints[spIndex], IntersectionControl.findIntersectionPoint(elem, cps[spIndex]), True) == 1:
                                counterPoint = IntersectionControl.findIntersectionPoint(elem, cps[spIndex])
                                counterPoint.append(0)
                                counterpoint_dict[cpsIndex].append(counterPoint)
                            elif IntersectionControl.orientation(segment.startPoint, segment.checkpoints[spIndex], IntersectionControl.findIntersectionPoint(elem, cps[spIndex]), True) == 2:
                                counterPoint = IntersectionControl.findIntersectionPoint(elem, cps[spIndex])
                                counterPoint.append(1)
                                counterpoint_dict[cpsIndex].append(counterPoint)

        counter = 0
        for nameIndex, elem in enumerate(self.lineNames):
            temp_list = []
            if nameIndex != index:
                for cpIndex, cp in enumerate(counterpoint_dict[counter]):
                    if cp != 0:
                        if cp[2] == 1:
                            temp_list.append(round(0-(Calculator.haversine_algorithm(cp, self.checkpoints[index][cpIndex]) * 1000), 2))
                        elif cp[2] == 0:
                            temp_list.append(round((Calculator.haversine_algorithm(cp, self.checkpoints[index][cpIndex]) * 1000), 2))
                    else:
                        temp_list.append("-")
                distance_dict[elem] = temp_list
                counter = counter + 1
        self.output_to_excell(index, distance_dict)

    def output_to_excell(self, index, distance_dict):
        file_name = "./output/" + self.lineNames[index] + ".xlsx"
        df = pd.DataFrame.from_dict(distance_dict, orient='index')
        df = df.transpose()
        df.to_excel(file_name, index=False)


if __name__ == "__main__":
    Main().main()

from os import path

from ReadKml import *
from Calculator import Calculator as calc
from TypeConverter import *
from CartesianCalculator import CartesianCalculator as ccalc
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
            self.coordinateList.append(TypeConverter.stringListtoFloatList(str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))
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
        # checkpoint = ccalc.find_checkpoint(self.coordinateList[0][1], self.coordinateList[0][2], 1)
        # print("Kartezyen " + str(checkpoint))
        # print("2. Nokta = " + str(
        #    ccalc.find_second_point(self.coordinateList[0][1], self.checkpoints[0][0], self.coordinateList[1][1],
        #                            self.coordinateList[1][2])))

    @staticmethod
    def find_checkpoints(coordinates):
        temp_list = []
        checkpoint_distance = 1
        j = 0
        checkpoint = coordinates[0].startPoint
        while j < len(coordinates):
            if calc.haversine_algorithm(checkpoint, coordinates[j].endPoint) >= checkpoint_distance:
                checkpoint = calc.find_second_point(checkpoint,
                                                    calc.calculate_bearing(checkpoint, coordinates[j].endPoint),
                                                    checkpoint_distance)
                checkpoint_distance = 1
                temp_list.append(checkpoint)
            else:
                checkpoint_distance = checkpoint_distance - calc.haversine_algorithm(checkpoint,
                                                                                     coordinates[j].endPoint)
                checkpoint = coordinates[j].endPoint
                j = j + 1
        return temp_list


if __name__ == "__main__":
    Main().main()

from os import path

from ReadKml import *
from Calculator import *
from TypeConverter import *
from CartesianCalculator import *


class Main:
    distance = 0
    floatList0 = []
    floatList1 = []
    kml_files = []
    roots = []
    coordinates = []
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
            self.coordinates.append(TypeConverter.stringListtoFloatList(
                str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))
        for c in self.coordinates:
            self.checkpoints.append(self.find_checkpoints(c))
        print("Kartezyen Mesafe " + str(
            CartesianCalculator.calculate_distance(self.coordinates[0][0], self.coordinates[0][1])))
        print("Coğrafi Mesafe " + str(Calculator.haversine_algorithm(self.coordinates[0][0], self.coordinates[0][1])))
        print("Kartezyen " + str(
            CartesianCalculator.find_second_point(self.coordinates[0][0], self.coordinates[0][1], 1)))
        print("Coğrafi " + str(Calculator.find_second_point(self.coordinates[0][0],
                                                            Calculator.calculate_bearing(self.coordinates[0][0],
                                                                                         self.coordinates[0][1]), 1)))
        print("Hata payı = " + str((Calculator.haversine_algorithm(self.coordinates[0][0], self.coordinates[0][1])
                                    - CartesianCalculator.calculate_distance(self.coordinates[0][0], self.coordinates[0][1]))
                                   / Calculator.haversine_algorithm(self.coordinates[0][0], self.coordinates[0][1])))

    @staticmethod
    def find_checkpoints(coordinates):
        temp_list = []
        checkpoint_distance = 1
        j = 0
        checkpoint = coordinates[0]
        while j + 1 < len(coordinates):
            if Calculator.haversine_algorithm(checkpoint, coordinates[j + 1]) >= checkpoint_distance:
                checkpoint = Calculator.find_second_point(checkpoint,
                                                          Calculator.calculate_bearing(checkpoint, coordinates[j + 1]),
                                                          checkpoint_distance)
                checkpoint.append(j)
                checkpoint_distance = 1
                temp_list.append(checkpoint)
            else:
                checkpoint_distance = checkpoint_distance - Calculator.haversine_algorithm(checkpoint,
                                                                                           coordinates[j + 1])
                checkpoint = coordinates[j + 1]
                j = j + 1
        return temp_list


if __name__ == "__main__":
    Main().main()

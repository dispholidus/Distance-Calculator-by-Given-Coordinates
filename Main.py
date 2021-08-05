from os import path

from ReadKml import *
from Calculator import *
from TypeConverter import *


class Main:
    LATITUDE_DISTANCE = 111
    line = [0, 0, 0, 0]
    distance = 0
    floatList0 = []
    floatList1 = []
    kml_files = []
    roots = []
    coordinates = []

    def __init__(self):
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR KUZEY.kml"))
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR GUNEY(1).kml"))

    def main(self):
        # kml dosyalarının içine xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" eklemeyi unutma
        # kml dosyalarının kordinat kısmında ki tüm boşlukları sil

        for k in self.kml_files:
            self.roots.append(ReadKml.read(k))
        for r in self.roots:
            self.coordinates.append(TypeConverter.stringListtoFloatList(str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))

        x_distance = Calculator.find_x_distance(self.coordinates[0][0], self.coordinates[0][1], 10)
        x_degree = self.coordinates[0][0][0] + Calculator.meter_to_degree(Calculator.calc_longtitude_distance(self.coordinates[0][0][1]), x_distance)
        y_degree = Calculator.find_latitude(x_degree, self.coordinates[0][0], self.coordinates[0][1])
        print(str(x_distance) + "\n" + str(x_degree) + "\n" + str(y_degree))
        self.distance = Calculator.haversine_algorithm(self.coordinates[0][0], [x_degree, y_degree])
        print(self.distance)


if __name__ == "__main__":
    Main().main()

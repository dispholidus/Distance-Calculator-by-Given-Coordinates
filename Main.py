from os import path

from ReadKml import *
from FindDistance import *
from TypeConverter import *


class Main:
    line = [0, 0, 0, 0]
    distance = 0
    floatList0 = []
    floatList1 = []
    kml_files = []
    roots = []
    coordinates = []

    def __init__(self):
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR GUNEY(1).kml"))
        self.kml_files.append(path.join("KMLDosyaları/Hat_380kV_GELIBOLU 380 - UNIMAR KUZEY.kml"))

    def main(self):
        # kml dosyalarının içine xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" eklemeyi unutma
        # kml dosyalarının kordinat kısmında ki tüm boşlukları sil
        for k in self.kml_files:
            self.roots.append(ReadKml.read(k))
        for r in self.roots:
            self.coordinates.append(TypeConverter.stringListtoFloatList(
                str(r.Document.Placemark.MultiGeometry.LineString.coordinates).split(" ")))
        distance = FindDistance.haversine_algorithm(self.coordinates[0][0], self.coordinates[1][0])
        print(distance)


if __name__ == "__main__":
    Main().main()

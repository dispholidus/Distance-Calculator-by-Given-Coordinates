from pykml import parser
import re


class ReadKml:

    @staticmethod
    def read(file):
        ReadKml.fixFile(file)
        with open(file, encoding="UTF-8") as f:
            doc = f.read().encode("UTF-8")
            root = parser.fromstring(doc)
        return root

    @staticmethod
    def fixFile(file):
        f = open(file, mode="r", encoding="UTF-8")
        list_of_lines = f.readlines()
        secondLine = list_of_lines[1]
        secondLine = re.sub(r'xmlns:atom="http://www.w3.org/2005/Atom">', 'xmlns:atom="http://www.w3.org/2005/Atom" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
                            secondLine, flags=re.IGNORECASE)
        list_of_lines[1] = secondLine
        f = open(file, mode="w", encoding="UTF-8")
        f.writelines(list_of_lines)
        f.close()



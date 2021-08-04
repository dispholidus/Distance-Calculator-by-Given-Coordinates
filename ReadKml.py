from pykml import parser


class ReadKml:

    @staticmethod
    def read(file):
        with open(file, encoding="UTF-8") as f:
            doc = f.read().encode("UTF-8")
            root = parser.fromstring(doc)
        return root

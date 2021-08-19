import re


class TypeConverter:

    @staticmethod
    def stringListtoFloatList(stringList):
        stringList = TypeConverter.fixList(stringList)
        floatList = []
        for i in stringList:
            tempList = i.split(",")
            count = 0
            for j in tempList:
                tempList[count] = float(j)
                count = count + 1
            floatList.append(tempList)
        return floatList

    @staticmethod
    def fixList(stringList):
        for index, i in enumerate(stringList):
            stringList[index] = re.sub(r'\t', '', i)
        for index, i in enumerate(stringList):
            stringList[index] = re.sub(r'\n', '', i)
            if index == len(stringList)-1:
                stringList.remove("")
        return stringList

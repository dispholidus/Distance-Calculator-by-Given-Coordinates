class TypeConverter:

    @staticmethod
    def stringListtoFloatList(stringList):
        floatList = []
        for i in stringList:
            tempList = i.split(",")
            count = 0
            for j in tempList:
                tempList[count] = float(j)
                count = count + 1
            floatList.append(tempList)
        return floatList

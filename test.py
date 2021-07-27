from DO.Table import Table

if __name__ == '__main__':

    tableList = []
    for i in range(2):
        newTable = Table()
        newTable.fieldDic.update( {"1":"2"})
        tableList.append(newTable)

    for table in tableList:
        print(table.fieldDic)

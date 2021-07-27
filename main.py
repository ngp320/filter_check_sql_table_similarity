import os
import re

from loguru import logger

from DO.Table import Table
from utils.setLoguru import setLoguru


def readFile2Dic():
    tableList = []
    srcTableList = []
    # topdown --可选，为 True，则优先遍历 top 目录，否则优先遍历 top 的子目录(默认为开启)。如果 topdown 参数为 True，walk 会遍历top文件夹，与top 文件夹中每一个子目录。
    for root, dirs, files in os.walk("sql_comp", topdown=False):
        for file in files:
            with open('./sql_comp/' + file, encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    processEachLine(line, tableList)

    for root, dirs, files in os.walk("sql_src", topdown=False):
        for file in files:
            with open('./sql_src/' + file, encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    processEachLine(line, srcTableList)

    return tableList, srcTableList


def processEachLine(line, tableList):
    global currentTable

    # 识别表名
    tableName = re.findall(r'CREATE TABLE .([a-zA-Z_0-9]+).', line)
    if len(tableName) != 0:
        if currentTable != None:
            if currentTable.get_fieldDic() != {}:
                logger.debug(currentTable.tableName)
                logger.debug(currentTable.get_fieldDic())
                tableList.append(currentTable)
        processTableName(tableName)
        #  处理完一个 table时, 把数据放入 tableList, 这里通过判断 空集合 来 判断

    # 识别字段
    # 2空格+1非字母数字下划线+n个字母数字下划线+1非字母数字下划线+1空格
    fieldNameAndComment = re.findall(r'[ ]{2}[^\w]([\w]+)[^\w][ ]{1}.*COMMENT..(.*)\'', line)
    if len(fieldNameAndComment) != 0:
        currentTable.get_fieldDic().update(dict(fieldNameAndComment))


# 基本把tableName存入new的一个Table() 并 currentTable = newTable
def processTableName(tableName):
    global currentTable
    newTable = Table()
    currentTable = newTable

    # 如果表名不为空 则 保存入newTable
    tableName = tableName[0]
    currentTable.tableName = tableName
    logger.debug("tableName " + "#" * 30 + " {}".format(tableName))


# 获取 str 相似度
def check_similarity(str1, str2):
    import difflib
    similarity = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
    # print(similarity)	# 0.6666666666666666
    return similarity


# 检查表的相似度
def check_table_similarity(targetTable, compare_table):
    logger.debug(
        "#" * 10 + "{} <>---<> {} ".format(targetTable.get_tableName(), compare_table.get_tableName()) + "#" * 10)

    for t_key, t_val in targetTable.get_fieldDic().items():
        for ct_key, ct_val in compare_table.get_fieldDic().items():
            if ct_key == t_key and ct_val == t_val:
                compare_table.similarity_count += 2
                logger.debug("{},{} <---> {},{} ".format(ct_key, ct_val, ct_key, ct_val))

    for t_field in targetTable.get_fieldDic().keys():
        for ct_field in compare_table.get_fieldDic().keys():
            if check_similarity(t_field, ct_field) > 0.95:
                compare_table.similarity_count += 1
                logger.debug("{} <---> {} ".format(t_field, ct_field))

    for t_value in targetTable.get_fieldDic().values():
        for ct_value in compare_table.get_fieldDic().values():
            if check_similarity(t_value, ct_value) > 0.95:
                compare_table.similarity_count += 1
                logger.debug("{} <---> {} ".format(ct_value, ct_value))


# 用表名 获取 该表的table的数据结构
def getTargetTable(targetTable_name):
    for table in srcTableList:
        if table.tableName == targetTable_name:
            return table


if __name__ == '__main__':

    # 初始参数 用于识别 每个表放入Table类
    currentTable = None
    # 初始化 logger
    setLoguru()
    # 读取文件, 分为 源table 和 目标table
    comp_tableList, srcTableList = readFile2Dic()

    # 获取 需要查询的表
    print()
    targetTable_name = input("请输入表名, 查询相似表: ")
    print()
    targetTable = getTargetTable(targetTable_name)
    if targetTable is None:
        raise Exception("没找到 查询表")

    # 查询
    for compare_table in comp_tableList:
        # print(table.tableName)
        # print(table.get_fieldDic())
        check_table_similarity(targetTable, compare_table)

    comp_tableList.sort(key=lambda x: x.similarity_count, reverse=True)

    resList = comp_tableList[:10]
    resList.reverse()
    for res_comp_table in resList:
        logger.info("相似表: {} --------- 相似度 {}".format(res_comp_table.tableName, res_comp_table.similarity_count))
        check_table_similarity(targetTable, res_comp_table)

    logger.info("相似度 按 倒序排列")
    logger.info("logs/runtime.log 中 可以查看 具体那些值相同")

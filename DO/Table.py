class Table:
    def __init__(self):
        self.tableName = ""
        self.fieldDic = {}
        self.similarity_count = 0

    def get_tableName(self):
        return self.tableName

    def set_fieldDic(self, fieldDic):
        self.fieldDic = fieldDic

    def get_fieldDic(self):
        return self.fieldDic

    def get_similarity_count(self):
        return self.similarity_count

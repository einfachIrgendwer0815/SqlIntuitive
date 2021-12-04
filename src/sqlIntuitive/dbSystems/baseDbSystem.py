from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType

class BaseDbSystem():
    placeholder = "%s"
    
    def __init__(self, database: str, adaptionProvider: AdaptionProvider = None) -> None:
        self.database = database

        if isinstance(adaptionProvider, AdaptionProvider):
            self.adaptProvider = adaptionProvider
        else:
            self.adaptProvider = AdaptionProvider()

        self.dbCon = None
        self.cursor = None

    def addDataType(self, dataType: CustomDataType) -> None:
        self.adaptProvider.addDataType(dataType)

    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        self.adaptProvider.addDataType_raw(name, cls, clsToStringFunc, stringToClsFunc)

    def create_table(self, tableName: str, columns: dict, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> None:
        sql = sqlGeneration.gen_create_table(tableName, columns, primaryKeys=primaryKeys, foreignKeys=foreignKeys, namedForeignKeys=namedForeignKeys, uniqueColumns=uniqueColumns, safeMode=safeMode)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def drop_table(self, tableName: str) -> None:
        sql = sqlGeneration.gen_drop_table(tableName)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def insert_into(self, tableName: str, column_values: dict) -> None:
        adaptedColumnValues = self.adaptProvider.convertDictToString(column_values)

        sql, column_values_ordered = sqlGeneration.gen_insert(tableName, adaptedColumnValues, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def update(self, tableName: str, newColumnValues: dict, conditions: dict = {}, conditionCombining: str = "AND") -> None:
        adaptedNewColumnValues = self.adaptProvider.convertDictToString(newColumnValues)
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_update(tableName=tableName, newValues=adaptedNewColumnValues, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def delete_from(self, tableName: str, conditions: dict = {}, conditionCombining: str = "AND") -> None:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_delete(tableName=tableName, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def select_from(self, tableName: str, columns: list = [], conditions: dict = {}, conditionCombining: str = "AND") -> list:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_select(tableName=tableName, columns=columns, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        for index in range(len(res)):
            res[index] = self.adaptProvider.convertTupleToClsInstance(res[index])

        return res

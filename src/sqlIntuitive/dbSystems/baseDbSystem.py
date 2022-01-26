from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes
from sqlIntuitive.dbSystems.supportTracker import ifSupported, Features, isSupported
from sqlIntuitive.exceptions import CursorIsNone

def cursorNotNone(func):
    def inner(self, *args, **kwargs):
        if self.__getattribute__('cursor') != None:
            return func(self, *args, **kwargs)

        raise CursorIsNone()

    return inner

class BaseDbSystem():
    placeholder = "%s"
    SUPPORTS = Features.ALL.value

    def __init__(self, database: str, adaptionProvider: AdaptionProvider = None) -> None:
        self.database = database

        if isinstance(adaptionProvider, AdaptionProvider):
            self.adaptProvider = adaptionProvider
        else:
            self.adaptProvider = AdaptionProvider()

        self.dbCon = None
        self.cursor = None

    def supports(self, feature: Features) -> bool:
        return isSupported(feature, self.SUPPORTS)

    @ifSupported(Features.ADDON_CUSTOM_DATA_TYPE)
    def addDataType(self, dataType: CustomDataType) -> None:
        self.adaptProvider.addDataType(dataType)

    @ifSupported(Features.ADDON_CUSTOM_DATA_TYPE)
    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        self.adaptProvider.addDataType_raw(name, cls, clsToStringFunc, stringToClsFunc)

    @ifSupported(Features.SQL_CREATE_TABLE)
    @cursorNotNone
    def create_table(self, tableName: str, columns: dict, *, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> None:
        sql = sqlGeneration.standard.gen_create_table(tableName, columns, primaryKeys=primaryKeys, foreignKeys=foreignKeys, namedForeignKeys=namedForeignKeys, uniqueColumns=uniqueColumns, safeMode=safeMode)

        self.cursor.execute(sql)

        self.dbCon.commit()

    @ifSupported(Features.SQL_DROP_TABLE)
    @cursorNotNone
    def drop_table(self, tableName: str) -> None:
        sql = sqlGeneration.standard.gen_drop_table(tableName)

        self.cursor.execute(sql)

        self.dbCon.commit()

    @ifSupported(Features.SQL_INSERT_INTO)
    @cursorNotNone
    def insert_into(self, tableName: str, column_values: dict) -> None:
        adaptedColumnValues = self.adaptProvider.convertDictToString(column_values)

        sql, column_values_ordered = sqlGeneration.standard.gen_insert(tableName, adaptedColumnValues, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_UPDATE)
    @cursorNotNone
    def update(self, tableName: str, newColumnValues: dict, conditions: dict = {}, *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> None:
        adaptedNewColumnValues = self.adaptProvider.convertDictToString(newColumnValues)
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.standard.gen_update(tableName=tableName, newValues=adaptedNewColumnValues, conditions=adaptedConditions, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_DELETE_FROM)
    @cursorNotNone
    def delete_from(self, tableName: str, conditions: dict = {}, *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> None:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.standard.gen_delete(tableName=tableName, conditions=adaptedConditions, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_SELECT_FROM)
    @cursorNotNone
    def select_from(self, tableName: str, columns: list = [], conditions: dict = {}, *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> list:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.standard.gen_select(tableName=tableName, columns=columns, conditions=adaptedConditions, distinct=distinct, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        for index in range(len(res)):
            res[index] = self.adaptProvider.convertTupleToClsInstance(res[index])

        return res

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_count(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> int:
        return self._select_count_avg_sum(mode=sqlGeneration.standard.Count_avg_sum_modes.COUNT, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_avg(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> float:
        return self._select_count_avg_sum(mode=sqlGeneration.standard.Count_avg_sum_modes.AVG, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_sum(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> float:
        return self._select_count_avg_sum(mode=sqlGeneration.standard.Count_avg_sum_modes.SUM, tableName=tableName, column=column, conditions=conditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    @cursorNotNone
    def _select_count_avg_sum(self, mode: sqlGeneration.standard.Count_avg_sum_modes, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, distinct: bool = False, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO):
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.standard.gen_count_avg_sum(mode=mode, tableName=tableName, column=column, conditions=adaptedConditions, distinct=distinct, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        return res[0][0]

    @ifSupported(Features.SQL_STORED_PROCEDURES)
    @cursorNotNone
    def create_procedure(self, procedureName: str, sql_statement: str, parameters: dict = {}) -> None:
        adaptedParameters = self.adaptionProvider.convertDictToString(parameters)

        sql = sqlGeneration.standard.gen_create_stored_procedure(procedureName=procedureName, sql_statement=sql_statement, parameters=adaptedParameters, placeholder=self.placeholder)

        self.cursor.execute(sql)

    @ifSupported(Features.SQL_STORED_PROCEDURES)
    @cursorNotNone
    def exec_procedure(self,  procedureName: str, parameters: dict = {}) -> list:
        adaptedParameters = self.adaptionProvider.convertDictToString(parameters)

        sql, values_ordered = sqlGeneration.standard.gen_exec_procedure(procedureName=procedureName, parameters=adaptedParameters, placeholder=self.placeholder)

        self.cursor.execute(sql, values_ordered)

        res = self.cursor.fetchall()

        return res

    @ifSupported(Features.SQL_STORED_PROCEDURES)
    @cursorNotNone
    def drop_procedure(self, procedureName: str) -> None:
        sql = sqlGeneration.standard.gen_drop_procedure(procedureName)

        self.cursor.execute(sql)

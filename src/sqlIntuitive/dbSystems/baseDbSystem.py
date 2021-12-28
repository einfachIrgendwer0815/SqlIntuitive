from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes
from sqlIntuitive.dbSystems.supportTracker import ifSupported, Features, isSupported

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
    def create_table(self, tableName: str, columns: dict, *, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> None:
        sql = sqlGeneration.gen_create_table(tableName, columns, primaryKeys=primaryKeys, foreignKeys=foreignKeys, namedForeignKeys=namedForeignKeys, uniqueColumns=uniqueColumns, safeMode=safeMode)

        self.cursor.execute(sql)

        self.dbCon.commit()

    @ifSupported(Features.SQL_DROP_TABLE)
    def drop_table(self, tableName: str) -> None:
        sql = sqlGeneration.gen_drop_table(tableName)

        self.cursor.execute(sql)

        self.dbCon.commit()

    @ifSupported(Features.SQL_INSERT_INTO)
    def insert_into(self, tableName: str, column_values: dict) -> None:
        adaptedColumnValues = self.adaptProvider.convertDictToString(column_values)

        sql, column_values_ordered = sqlGeneration.gen_insert(tableName, adaptedColumnValues, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_UPDATE)
    def update(self, tableName: str, newColumnValues: dict, conditions: dict = {}, *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> None:
        adaptedNewColumnValues = self.adaptProvider.convertDictToString(newColumnValues)
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_update(tableName=tableName, newValues=adaptedNewColumnValues, conditions=adaptedConditions, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_DELETE_FROM)
    def delete_from(self, tableName: str, conditions: dict = {}, *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> None:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_delete(tableName=tableName, conditions=adaptedConditions, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    @ifSupported(Features.SQL_SELECT_FROM)
    def select_from(self, tableName: str, columns: list = [], conditions: dict = {}, *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO) -> list:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_select(tableName=tableName, columns=columns, conditions=adaptedConditions, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        for index in range(len(res)):
            res[index] = self.adaptProvider.convertTupleToClsInstance(res[index])

        return res

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_count(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO):
        return self._select_count_avg_sum(mode=sqlGeneration.Count_avg_sum_modes.COUNT, tableName=tableName, column=column, conditions=conditions, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_avg(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO):
        return self._select_count_avg_sum(mode=sqlGeneration.Count_avg_sum_modes.AVG, tableName=tableName, column=column, conditions=conditions, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def select_sum(self, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO):
        return self._select_count_avg_sum(mode=sqlGeneration.Count_avg_sum_modes.SUM, tableName=tableName, column=column, conditions=conditions, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison)

    @ifSupported(Features.SQL_COUNT_AVG_SUM)
    def _select_count_avg_sum(self, mode: sqlGeneration.Count_avg_sum_modes, tableName: str, column: str = "", conditions: dict = {}, combinations: list = [], *, conditionCombining: CombinationTypes = CombinationTypes.AND, conditionComparison: ComparisonTypes = ComparisonTypes.EQUAL_TO):
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_count_avg_sum(mode=mode, tableName=tableName, column=column, conditions=conditions, combinations=combinations, conditionCombining=conditionCombining, conditionComparison=conditionComparison, placeholder=self.placeholder)

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        return res[0][0]

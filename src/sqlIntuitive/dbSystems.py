from mysql.connector import connection
from mysql.connector import Error

from time import sleep

from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType

class SqliteDbSystem():
    pass

class MySqlDbSystem():
    def __init__(self, host: str, database: str, username: str, password: str, adaptionProvider: AdaptionProvider = None, max_connect_retries: int = 5) -> None:
        self.host = host
        self.database = database
        self.username = username
        self.password = password

        if isinstance(adaptionProvider, AdaptionProvider):
            self.adaptProvider = adaptionProvider
        else:
            self.adaptProvider = AdaptionProvider()

        self.dbCon = None
        self.cursor = None
        self.max_connect_retries = max_connect_retries

    def addDataType(self, dataType: CustomDataType) -> None:
        self.adaptProvider.addDataType(dataType)

    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        self.adaptProvider.addDataType_raw(name, cls, clsToStringFunc, stringToClsFunc)

    def connect_to_db(self, retryNo: int = 0, timeout: int = 3) -> bool:
        if self.dbCon != None: return False

        try:
            self.dbCon = connection.MySQLConnection(
                host=self.host,
                database=self.database,
                username=self.username,
                password=self.password
            )
        except Error as e:
            sleep(timeout)

            if retryNo >= self.max_connect_retries or self.connect_to_db(retryNo+1) == False:
                return False

        return True

    def close_connection(self) -> None:
        if self.dbCon != None and self.dbCon.is_connected():
            self.dbCon.close()

    def create_cursor(self) -> None:
        if self.cursor != None or self.dbCon == None or self.dbCon.is_connected() == False:
            return

        self.cursor = self.dbCon.cursor()

    def create_table(self, tableName: str, columns: list, primaryKeys: list = [], foreignKeys: dict = {}, namedForeignKeys: dict = {}, uniqueColumns: list = [], safeMode: bool = True) -> None:
        sql = sqlGeneration.gen_create_table(tableName, columns, primaryKeys=primaryKeys, foreignKeys=foreignKeys, namedForeignKeys=namedForeignKeys, uniqueColumns=uniqueColumns, safeMode=safeMode)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def drop_table(self, tableName: str) -> None:
        sql = sqlGeneration.gen_drop_table(tableName)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def insert_into(self, tableName: str, column_values: dict) -> None:
        adaptedColumnValues = self.adaptProvider.convertDictToString(column_values)

        sql, column_values_ordered = sqlGeneration.gen_insert(tableName, adaptedColumnValues, placeholder="%s")

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def update(self, tableName: str, newColumnValues: dict, conditions: dict = {}, conditionCombining: str = "AND") -> None:
        adaptedNewColumnValues = self.adaptProvider.convertDictToString(newColumnValues)
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_update(tableName=tableName, newValues=adaptedNewColumnValues, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def delete_from(self, tableName: str, conditions: dict = {}, conditionCombining: str = "AND") -> None:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_delete(tableName=tableName, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def select_from(self, tableName: str, columns: list = [], conditions: dict = {}, conditionCombining: str = "AND") -> list:
        adaptedConditions = self.adaptProvider.convertDictToString(conditions)

        sql, column_values_ordered = sqlGeneration.gen_select(tableName=tableName, columns=columns, conditions=adaptedConditions, conditionCombining=conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        res = self.cursor.fetchall()

        for index in range(len(res)):
            res[index] = self.adaptProvider.convertTupleToClsInstance(res[index])

        return res

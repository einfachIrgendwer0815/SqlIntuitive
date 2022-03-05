from mysql.connector import connection
from mysql.connector import Error

from time import sleep

from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType
from sqlIntuitive.dbSystems import BaseDbSystem
from sqlIntuitive.dbSystems.baseDbSystem import cursorNotNone
from sqlIntuitive.dbSystems.supportTracker import or_values, Features, ifSupported

class MySqlDbSystem(BaseDbSystem):
    placeholder = "%s"
    SUPPORTS = or_values([
        Features.SQL_CREATE_TABLE,
        Features.SQL_DROP_TABLE,
        Features.SQL_ALTER_TABLE_ADD,
        Features.SQL_ALTER_TABLE_DROP,
        Features.SQL_ALTER_TABLE_MODIFY,
        Features.SQL_INSERT_INTO,
        Features.SQL_UPDATE,
        Features.SQL_DELETE_FROM,
        Features.SQL_SELECT_FROM,
        Features.SQL_COUNT_AVG_SUM,
        Features.SQL_PRIMARY_KEYS,
        Features.SQL_FOREIGN_KEYS,
        Features.SQL_FOREIGN_KEYS_CUSTOM_CONSTRAINT,
        Features.SQL_UNIQUE,
        Features.ADDON_CUSTOM_DATA_TYPE
        ])

    def __init__(self, host: str, database: str, username: str, password: str, adaptionProvider: AdaptionProvider = None, max_connect_retries: int = 5) -> None:
        super().__init__(database, adaptionProvider)

        self.host = host
        self.username = username
        self.password = password
        self.max_connect_retries = max_connect_retries

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

    @ifSupported(Features.SQL_ALTER_TABLE_MODIFY)
    @cursorNotNone
    def alter_table_modify(self, tableName: str, column_name: str, column_type: str) -> None:
        sql = sqlGeneration.mysql.gen_alter_table_modify(tableName, column_name, column_type)

        self.cursor.execute(sql)

        self.dbCon.commit()

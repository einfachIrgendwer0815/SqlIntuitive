import sqlite3

from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType
from sqlIntuitive.dbSystems import BaseDbSystem
from sqlIntuitive.dbSystems.supportTracker import or_values, Features

class SqliteDbSystem(BaseDbSystem):
    placeholder="?"
    SUPPORTS = or_values([
        Features.SQL_CREATE_TABLE,
        Features.SQL_DROP_TABLE,
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

    def __init__(self, database: str, timeout: int = 5, adaptionProvider: AdaptionProvider = None):
        super().__init__(database, adaptionProvider)

        self.timeout = timeout
        self.open = False

    def addDataType(self, dataType: CustomDataType) -> None:
        self.adaptProvider.addDataType(dataType)

    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        self.adaptProvider.addDataType_raw(name, cls, clsToStringFunc, stringToClsFunc)

    def connect_to_db(self) -> None:
        if self.open == False:
            self.dbCon = sqlite3.connect(self.database, self.timeout)

            self.open = True

    def close_connection(self) -> None:
        if self.open != True:
            return

        if self.cursor != None:
            self.cursor.close()

        if self.dbCon != None:
            self.dbCon.close()

        self.open = False

    def create_cursor(self) -> None:
        if self.cursor != None or self.dbCon == None or self.open == False:
            return

        self.cursor = self.dbCon.cursor()

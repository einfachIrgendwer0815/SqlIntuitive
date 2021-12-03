import sqlite3

from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType

class SqliteDbSystem():
    def __init__(self, database: str, timeout: int = 5, adaptionProvider: AdaptionProvider = None):
        self.databaseFile = database

        if isinstance(adaptionProvider, AdaptionProvider):
            self.adaptProvider = adaptProvider
        else:
            self.adaptProvider = AdaptionProvider()

        self.timeout = timeout

        self.dbCon = None
        self.cursor = None

    def addDataType(self, dataType: CustomDataType) -> None:
        self.adaptProvider.addDataType(dataType)

    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        self.adaptProvider.addDataType_raw(name, cls, clsToStringFunc, stringToClsFunc)

    def connect_to_db(self) -> None:
        self.dbCon = sqlite3.connect(self.databaseFile, self.timeout)

    def close_connection(self) -> None:
        self.dbCon.close()

    def create_cursor(self) -> None:
        if self.cursor != None or self.dbCon == None:
            return

        self.cursor = self.dbCon.cursor()

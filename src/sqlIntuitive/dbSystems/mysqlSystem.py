from mysql.connector import connection
from mysql.connector import Error

from time import sleep

from sqlIntuitive import sqlGeneration
from sqlIntuitive.ext.customDataTypes import AdaptionProvider, CustomDataType
from sqlIntuitive.dbSystems import BaseDbSystem

class MySqlDbSystem(BaseDbSystem):
    placeholder = "%s"
    
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

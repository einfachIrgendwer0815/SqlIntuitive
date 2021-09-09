from mysql.connector import connection
from mysql.connector import Error

from time import sleep

from sqlIntuitive import sqlGeneration

class SqliteDbSystem():
    pass

class MySqlDbSystem():
    def __init__(self, host, database, username, password, max_connect_retries=5):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

        self.dbCon = None
        self.max_connect_retries = max_connect_retries

    def connect_to_db(self, retryNo=0, timeout=3):
        if self.dbCon != None: return False

        try:
            self.dbCon = connection.MySQLConnection(
                host=self.host,
                database=self.database,
                username=self.username,
                password=self.password
            )
        except Error as e:
            print(e)
            sleep(timeout)

            if retryNo >= self.max_connect_retries or self.connect_to_db(retryNo+1) == False:
                return False

        return True

    def close_connection(self):
        if self.dbCon != None and self.dbCon.is_connected():
            self.dbCon.close()

    def get_cursor(self):
        if self.dbCon == None or self.dbCon.is_connected() == False:
            return None

        return self.dbCon.cursor()

    def create_table(self, tableName, columns, safeMode=True):
        sql = sqlGeneration.gen_create_table(tableName, columns, safeMode=safeMode)

        cursor = self.get_cursor()

        cursor.execute(sql)

        self.dbCon.commit()

    def drop_table(self, tableName):
        sql = sqlGeneration.gen_drop_table(tableName)

        cursor = self.get_cursor()

        cursor.execute(sql)

        self.dbCon.commit()

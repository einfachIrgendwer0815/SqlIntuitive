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
        self.cursor = None
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

    def create_cursor(self):
        if self.cursor != None or self.dbCon == None or self.dbCon.is_connected() == False:
            return

        self.cursor = self.dbCon.cursor()

    def create_table(self, tableName, columns, safeMode=True):
        sql = sqlGeneration.gen_create_table(tableName, columns, safeMode=safeMode)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def drop_table(self, tableName):
        sql = sqlGeneration.gen_drop_table(tableName)

        self.cursor.execute(sql)

        self.dbCon.commit()

    def insert_into(self, tableName, column_values):
        sql, column_values_ordered = sqlGeneration.gen_insert(tableName, column_values, placeholder="%s")

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def update(self, tableName, newColumnValues, conditions={}, conditionCombining="AND"):
        sql, column_values_ordered = sqlGeneration.gen_update(tableName, newColumnValues, conditions, conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def delete_from(self, tableName, conditions={}, conditionCombining="AND"):
        sql, column_values_ordered = sqlGeneration.gen_delete(tableName, conditions, conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        self.dbCon.commit()

    def select_from(self, tableName, columns=[], conditions=[], conditionCombining="AND"):
        sql, column_values_ordered = sqlGeneration.gen_select(tableName, columns, conditions, conditionCombining, placeholder='%s')

        self.cursor.execute(sql, column_values_ordered)

        return self.cursor.fetchall()

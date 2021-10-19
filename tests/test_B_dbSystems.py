from sqlIntuitive import dbSystems

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestDBSystems = json.load(file)['dbSystems']

@unittest.skipIf(runTestDBSystems == False, 'Skipped TestDBSystems via config')
class TestDBSystems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tests/mysql_testserver_login.json', 'r') as file:
            cls.mysql_login = json.load(file)

        mydb = dbSystems.MySqlDbSystem(
            host=cls.mysql_login["host"],
            database=cls.mysql_login["database"],
            username=cls.mysql_login["username"],
            password=cls.mysql_login["password"],
        )

        mydb.connect_to_db()

        if mydb.dbCon.is_connected():
            cursor = mydb.dbCon.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS TableB (col1 varchar(10), col2 int PRIMARY KEY, col3 tinyint);")
        else:
            raise Exception()

        if mydb.dbCon != None and mydb.dbCon.is_connected():
            mydb.dbCon.close()

    def setUp(self):
        self.mydb = dbSystems.MySqlDbSystem(
            host=self.mysql_login["host"],
            database=self.mysql_login["database"],
            username=self.mysql_login["username"],
            password=self.mysql_login["password"],
        )

    def tearDown(self):
        if self.mydb.dbCon != None and self.mydb.dbCon.is_connected():
            self.mydb.dbCon.close()

    def test_A_connect_to_db(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.assertIsNotNone(self.mydb.dbCon)
        self.assertTrue(self.mydb.dbCon.is_connected())

        self.mydb.close_connection()

        self.assertFalse(self.mydb.dbCon.is_connected())

    def test_B_close_connection(self):
        self.assertIsNone(self.mydb.dbCon)

        self.mydb.close_connection()

        self.assertTrue(self.mydb.connect_to_db())

        self.mydb.close_connection()

        self.mydb.close_connection() # No close happens, but no error should appear.

    def test_C_get_cursor(self):
        self.assertTrue(self.mydb.connect_to_db())

        self.assertIsNone(self.mydb.cursor)

        self.mydb.create_cursor()

        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.close_connection()

    def test_D_create_table(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.create_table("TestA", {"name":"varchar(50)","id": "int", "id2": "int", "col3": 'int', "col4": "varchar(50)", "col5": "int"}, primaryKeys=['id', 'id2'], foreignKeys={'col3': 'TableB(col2)'}, namedForeignKeys={'col5': {'name':'myTestFK', 'reference': "TableB(col2)"}}, uniqueColumns=['col4'])

    def test_E_drop_table(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.drop_table("TestA")

    def test_F_insert_into(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.insert_into("TableB", {"col1": 'Test', "col2": 42, "col3": True})
        self.mydb.insert_into("TableB", {"col1": 'Test', "col2": 84, "col3": True})

    def test_G_update(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.update("TableB", {"col3": False, "col2": 43}, {"col2": 42})

    def test_H_select_from(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.select_from("TableB")

    def test_I_delete(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.delete_from("TableB", {"col2": 84})
        self.mydb.delete_from("TableB")

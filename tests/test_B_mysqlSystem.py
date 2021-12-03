from sqlIntuitive import dbSystems
from sqlIntuitive.ext import customDataTypes
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestMysqlSystem = json.load(file)['mysqlSystem']

@unittest.skipIf(runTestMysqlSystem == False, 'Skipped TestMysqlSystem via config')
class TestMysqlSystem(unittest.TestCase):
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

            cursor.execute("CREATE TABLE IF NOT EXISTS TableB (col1 varchar(200), col2 int PRIMARY KEY, col3 tinyint);")
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

        self.setUp()
        self.clearTableB()
        self.mydb.dbCon.close()

    def clearTableB(self):
        self.mydb.connect_to_db()
        cursor = self.mydb.dbCon.cursor()

        cursor.execute("DELETE FROM TableB;")
        self.mydb.dbCon.commit()

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
        self.mydb.update("TableB", {"col3": False, "col2": 44}, {"col2": {'value': 43, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}})

    def test_H_select_from(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.select_from("TableB")
        self.mydb.select_from("TableB", conditions={'col2': {'value':50, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}})

    def test_I_delete(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.delete_from("TableB", {"col2": 84})
        self.mydb.delete_from("TableB", {"col2": {'value': 80, 'comparison': ComparisonTypes.EQUAL_TO}})
        self.mydb.delete_from("TableB")

    def test_J_adaptionProvider(self):
        self.assertTrue(isinstance(self.mydb.adaptProvider, customDataTypes.AdaptionProvider))

        adaptProvider = customDataTypes.AdaptionProvider()
        mydb2 = dbSystems.MySqlDbSystem(
            host=self.mysql_login["host"],
            database=self.mysql_login["database"],
            username=self.mysql_login["username"],
            password=self.mysql_login["password"],
            adaptionProvider=adaptProvider
        )

        self.assertEqual(mydb2.adaptProvider, adaptProvider)

    def test_K_str_encoded(self):
        self.assertTrue(isinstance(self.mydb.adaptProvider, customDataTypes.AdaptionProvider))

        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.insert_into("TableB", {'col1': "CUSTOM;", 'col2': 6473573})

        res = self.mydb.select_from("TableB", columns=['col1'], conditions={'col2': 6473573})
        self.assertEqual(res, [("CUSTOM;",)])

    def test_L_customDataType(self):
        self.assertTrue(isinstance(self.mydb.adaptProvider, customDataTypes.AdaptionProvider))

        class TestClass():
            def __init__(self, num):
                self.num = num

        def testClassToString(instance):
            return str(instance.num)

        def stringToTestClass(string):
            return TestClass(int(string))

        dataType = customDataTypes.CustomDataType("TESTCLS", TestClass, testClassToString, stringToTestClass)

        self.mydb.addDataType(dataType)

        self.assertTrue('TESTCLS' in self.mydb.adaptProvider.types)

        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.insert_into("TableB", {'col1': TestClass(123), 'col2': 567})
        res = self.mydb.select_from("TableB", conditions={'col2': 567})

        self.assertTrue(isinstance(res[0][0], TestClass))

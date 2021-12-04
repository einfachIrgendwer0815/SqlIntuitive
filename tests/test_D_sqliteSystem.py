from sqlIntuitive import dbSystems
from sqlIntuitive.ext import customDataTypes

from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes

import sqlite3
import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

dbFile = "tests/test_D.db.sqlite3"

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqliteSystem = json.load(file)['sqliteSystem']

@unittest.skipIf(runTestSqliteSystem == False, 'Skipped TestSqliteSystem via config')
class TestSqliteSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        file_db = sqlite3.connect(dbFile)

        cursor = file_db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS TableA (col1 string, col2 int, col3 bool, col4 string, PRIMARY KEY (col1), UNIQUE (col4));")

        cursor.close()
        file_db.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(dbFile)

    def setUp(self):
        self.memory_db = dbSystems.SqliteDbSystem(database=":memory:")
        self.file_db = dbSystems.SqliteDbSystem(database=dbFile)

        self.memory_db.connect_to_db()
        self.file_db.connect_to_db()

    def tearDown(self):
        self.memory_db.close_connection()
        self.file_db.close_connection()

    def test_A_connect_to_db(self):
        self.assertIsNotNone(self.memory_db.dbCon)

    def test_B_cursor(self):
        self.assertIsNone(self.memory_db.cursor)

        self.memory_db.create_cursor()

        self.assertIsNotNone(self.memory_db.cursor)

    def test_C_adaptionProvider(self):
        self.assertTrue(isinstance(self.memory_db.adaptProvider, customDataTypes.AdaptionProvider))

        adaptProvider = customDataTypes.AdaptionProvider()
        memory_db2 = dbSystems.SqliteDbSystem(":memory:", adaptionProvider=adaptProvider)

        self.assertEqual(memory_db2.adaptProvider, adaptProvider)

    def test_D_open_close(self):
        self.memory_db.create_cursor() # Won't work but no error is raised

        self.memory_db.connect_to_db()
        self.memory_db.create_cursor()
        self.memory_db.close_connection()

        self.memory_db.create_cursor() # Won't work too but still no error is raised

    def test_E_create_table(self):
        self.file_db.create_cursor()

        self.file_db.create_table("TableB", {"name":"varchar(50)","id": "int", "id2": "int", "col3": 'int', "col4": "varchar(50)", "col5": "int"}, primaryKeys=['id', 'id2'], foreignKeys={'col3': 'TableB(col2)'}, namedForeignKeys={'col5': {'name':'myTestFK', 'reference': "TableB(col2)"}}, uniqueColumns=['col4'])

    def test_F_drop_table(self):
        self.file_db.create_cursor()

        self.file_db.drop_table("TableB")

    def test_G_insert_into(self):
        self.file_db.create_cursor()

        self.file_db.insert_into("TableA", {"col1": 'Test', "col2": 42, "col3": True})
        self.file_db.insert_into("TableA", {"col1": 'Test2', "col2": 84, "col3": True})


    def test_H_update(self):
        self.file_db.create_cursor()

        self.file_db.update("TableA", {"col3": False, "col2": 43}, {"col2": 42})
        self.file_db.update("TableA", {"col3": False, "col2": 44}, {"col2": {'value': 43, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}})

    def test_I_select_from(self):
        self.file_db.create_cursor()

        self.file_db.select_from("TableA")
        self.file_db.select_from("TableA", conditions={'col2': {'value':50, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}})

    def test_J_delete(self):
        self.file_db.create_cursor()

        self.file_db.delete_from("TableA", {"col2": 84})
        self.file_db.delete_from("TableA", {"col2": {'value': 80, 'comparison': ComparisonTypes.EQUAL_TO}})
        self.file_db.delete_from("TableA")

    def test_K_str_encoded(self):
        self.assertTrue(isinstance(self.file_db.adaptProvider, customDataTypes.AdaptionProvider))

        self.file_db.create_cursor()

        self.file_db.insert_into("TableA", {'col1': "CUSTOM;", 'col2': 6473573})

        res = self.file_db.select_from("TableA", columns=['col1'], conditions={'col2': 6473573})
        self.assertEqual(res, [("CUSTOM;",)])

    def test_L_customDataType(self):
        self.assertTrue(isinstance(self.file_db.adaptProvider, customDataTypes.AdaptionProvider))

        class TestClass():
            def __init__(self, num):
                self.num = num

        def testClassToString(instance):
            return str(instance.num)

        def stringToTestClass(string):
            return TestClass(int(string))

        dataType = customDataTypes.CustomDataType("TESTCLS", TestClass, testClassToString, stringToTestClass)

        self.file_db.addDataType(dataType)

        self.assertTrue('TESTCLS' in self.file_db.adaptProvider.types)

        self.file_db.create_cursor()

        self.file_db.insert_into("TableA", {'col1': TestClass(123), 'col2': 567})
        res = self.file_db.select_from("TableA", conditions={'col2': 567})

        self.assertTrue(isinstance(res[0][0], TestClass))

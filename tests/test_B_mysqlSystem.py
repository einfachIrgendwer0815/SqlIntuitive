from sqlIntuitive import dbSystems
from sqlIntuitive.ext import customDataTypes
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes
from sqlIntuitive.sqlGeneration.standard import Joins

from sqlIntuitive import exceptions

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

            cursor.execute("CREATE TABLE IF NOT EXISTS TableB (col1 varchar(200), col2 int PRIMARY KEY, col3 tinyint, col4 int);")
            cursor.execute("CREATE TABLE IF NOT EXISTS TableC (col1 varchar(200), col2 int PRIMARY KEY, col3 tinyint, col4 int);")
            cursor.execute("CREATE TABLE IF NOT EXISTS JoinTableA (col1 int, col2 varchar(10));")
            cursor.execute("CREATE TABLE IF NOT EXISTS JoinTableB (colA int, colB int, colC bool, colD varchar(10));")
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
        self.clearTables()
        self.mydb.dbCon.close()

    def clearTables(self):
        self.mydb.connect_to_db()
        cursor = self.mydb.dbCon.cursor()

        cursor.execute("DELETE FROM TableB;")
        cursor.execute("DELETE FROM TableC;")
        cursor.execute("DELETE FROM JoinTableA;")
        cursor.execute("DELETE FROM JoinTableB;")
        self.mydb.dbCon.commit()

    @classmethod
    def tearDownClass(cls):
        mydb = dbSystems.MySqlDbSystem(
            host=cls.mysql_login["host"],
            database=cls.mysql_login["database"],
            username=cls.mysql_login["username"],
            password=cls.mysql_login["password"],
        )

        mydb.connect_to_db()

        cursor = mydb.create_cursor()

        mydb.cursor.execute("DROP TABLE TableB;")
        mydb.cursor.execute("DROP TABLE TableC;")
        mydb.cursor.execute("DROP TABLE JoinTableA;")
        mydb.cursor.execute("DROP TABLE JoinTableB;")

        mydb.close_connection()

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

    def test_H_a_select_from(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.select_from("TableB")
        self.mydb.cursor.execute("INSERT INTO TableB (col1,col2) VALUES ('A',10),('B',20),('A',30);")

        res = self.mydb.select_from("TableB", ['col1'], conditions={'col2': {'value':50, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}})
        self.assertEqual(len(res), 3)

        res = self.mydb.select_from("TableB", ['col1'], conditions={'col2': {'value':50, 'comparison': ComparisonTypes.LESS_THAN_OR_EQUAL_TO}}, distinct=True)
        self.assertEqual(len(res), 2)

    def test_H_b_select_from(self):
        self.assertTrue(self.mydb.connect_to_db())
        self.mydb.create_cursor()
        self.assertIsNotNone(self.mydb.cursor)

        self.mydb.cursor.execute("INSERT INTO TableB (col1,col2) VALUES ('A',10),('B',20),('A',30),('C',40);")

        res = self.mydb.select_from("TableB", ['col1'], orderBy=['col2'])
        self.assertEqual(res, [('A',), ('B',), ('A',), ('C',)])

        res = self.mydb.select_from("TableB", ['col1'], orderBy=['col2'], orderDESC=True)
        self.assertEqual(res, [('C',), ('A',), ('B',), ('A',)])

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

    def test_M_select_count(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 1, 'col4': 123})
        self.mydb.insert_into("TableB", {'col1': "DEF", 'col2': 2, 'col4': 456})
        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 3, 'col4': 789})

        res = self.mydb.select_count("TableB", column="col4")
        self.assertEqual(res, 3)

        res = self.mydb.select_count("TableB", column="col4", conditions={"col1": "ABC"})
        self.assertEqual(res, 2)

        res = self.mydb.select_count("TableB", column="col4", conditions={"col4": {"value": 123, "comparison": ComparisonTypes.GREATER_THAN}})
        self.assertEqual(res, 2)


        res = self.mydb.select_count("TableB", column="col1")
        self.assertEqual(res, 3)

        res = self.mydb.select_count("TableB", column="col1", distinct=True)
        self.assertEqual(res, 2)

    def test_N_select_avg(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 1, 'col4': 123})
        self.mydb.insert_into("TableB", {'col1': "DEF", 'col2': 2, 'col4': 456})
        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 3, 'col4': 789})

        res = self.mydb.select_avg("TableB", column="col4")
        self.assertEqual(res, 456)

        res = self.mydb.select_avg("TableB", column="col4", conditions={"col1": "ABC"})
        self.assertEqual(res, (123+789)/2)

        res = self.mydb.select_avg("TableB", column="col4", conditions={"col4": {"value": 123, "comparison": ComparisonTypes.GREATER_THAN}})
        self.assertEqual(res, (456+789)/2)


        self.mydb.insert_into("TableB", {'col1': "GHI", 'col2': 4, 'col4': 123})

        res = self.mydb.select_avg("TableB", column="col4")
        self.assertEqual(res, (123+456+789+123)/4)

        res = self.mydb.select_avg("TableB", column="col4", distinct=True)
        self.assertEqual(res, (123+456+789)/3)

    def test_O_select_sum(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 1, 'col4': 123})
        self.mydb.insert_into("TableB", {'col1': "DEF", 'col2': 2, 'col4': 456})
        self.mydb.insert_into("TableB", {'col1': "ABC", 'col2': 3, 'col4': 789})

        res = self.mydb.select_sum("TableB", column="col4")
        self.assertEqual(res, 123+456+789)

        res = self.mydb.select_sum("TableB", column="col4", conditions={"col1": "ABC"})
        self.assertEqual(res, 123+789)

        res = self.mydb.select_sum("TableB", column="col4", conditions={"col4": {"value": 123, "comparison": ComparisonTypes.GREATER_THAN}})
        self.assertEqual(res, 456+789)


        self.mydb.insert_into("TableB", {'col1': "GHI", 'col2': 4, 'col4': 123})

        res = self.mydb.select_sum("TableB", column="col4")
        self.assertEqual(res, 123+456+789+123)

        res = self.mydb.select_sum("TableB", column="col4", distinct=True)
        self.assertEqual(res, 123+456+789)

    def test_P_cursorIsNone(self):
        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.create_table("TableB", {"col1": "string"})

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.drop_table("TableB")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.insert_into("TableB", {"col1": "abc"})

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.update("TableB", {"col1": "abc"})

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.delete_from("TableB")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.select_from("TableB")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.select_count("TableB", "col1")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.select_avg("TableB", "col1")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.select_sum("TableB", "col1")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.alter_table_add("TableB", "colABC", "int")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.alter_table_drop("TableB", "colABC")

        with self.assertRaises(exceptions.CursorIsNone):
            self.mydb.alter_table_modify("TableB", "colABC", "int")

    def test_Q_alter_table_add(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.alter_table_add("TableC", "col123", "int")

    def test_R_alter_table_drop(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.alter_table_drop("TableC", "col1")

    def test_S_alter_table_add(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.alter_table_modify("TableC", "col4", "varchar(10)")

    def test_T_select_join(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        self.mydb.cursor.execute("INSERT INTO JoinTableA (col1, col2) VALUES (1,'A'),(2,'ABC'),(4, 'random'),(5,'qwertz');")
        self.mydb.cursor.execute("INSERT INTO JoinTableB (colA, colB, colC, colD) VALUES (1,123, 1, 'mno'),(2,987, 0, 'modnar'),(3, 634125, 0, 'xyz'),(4, 456, 1, 'DEF');")

        self.assertEqual(
            self.mydb.select_join(Joins.INNER_JOIN, 'JoinTableA', ['col1', 'col2'], 'JoinTableB', ['colB', 'colC', 'colD'], 'col1', 'colA'),
            [
                (1, 'A', 123, True, 'mno'),
                (2, 'ABC', 987, False, 'modnar'),
                (4, 'random', 456, True, 'DEF')
            ]
        )

        self.assertEqual(
            self.mydb.select_join(Joins.LEFT_JOIN, 'JoinTableA', ['col1', 'col2'], 'JoinTableB', ['colB', 'colC', 'colD'], 'col1', 'colA'),
            [
                (1, 'A', 123, True, 'mno'),
                (2, 'ABC', 987, False, 'modnar'),
                (4, 'random', 456, True, 'DEF'),
                (5, 'qwertz', None, None, None)
            ]
        )

        self.assertEqual(
            self.mydb.select_join(Joins.RIGHT_JOIN, 'JoinTableA', ['col1', 'col2'], 'JoinTableB', ['colB', 'colC', 'colD'], 'col1', 'colA'),
            [
                (1, 'A', 123, True, 'mno'),
                (2, 'ABC', 987, False, 'modnar'),
                (None, None, 634125, False, 'xyz'),
                (4, 'random', 456, True, 'DEF')
            ]
        )

    def test_U_select_join(self):
        self.mydb.connect_to_db()
        self.mydb.create_cursor()

        with self.assertRaises(exceptions.NotSupported):
            self.mydb.select_join(Joins.FULL_JOIN, 'JoinTableA', ['col1', 'col2'], 'JoinTableB', ['colB', 'colC', 'colD'], 'col1', 'colA')

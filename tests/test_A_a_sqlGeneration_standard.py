from sqlIntuitive import exceptions
from sqlIntuitive.sqlGeneration import standard
from sqlIntuitive.conditionEnums import ComparisonTypes, CombinationTypes

import unittest

import random, string

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqlGenerationStandard = json.load(file)['sqlGeneration_standard']

@unittest.skipIf(runTestSqlGenerationStandard == False, 'Skipped TestSqlGenerationStandard via config')
class TestSqlGenerationStandard(unittest.TestCase):
    def test_A_A_a_gen_conditions(self):
        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}), ('abc=? AND xyz=? AND test>?', ['def', 123, 42]))
        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, defaultComparison=ComparisonTypes.LESS_THAN_OR_EQUAL_TO), ('abc<=? AND xyz<=? AND test>?', ['def', 123, 42]))
        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, defaultCombination=CombinationTypes.OR), ('abc=? OR xyz=? OR test>?', ['def', 123, 42]))

        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, combinations=[CombinationTypes.OR]), ('abc=? OR xyz=? AND test>?', ['def', 123, 42]))
        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, combinations=[CombinationTypes.OR, CombinationTypes.AND, CombinationTypes.OR]), ('abc=? OR xyz=? AND test>?', ['def', 123, 42]))

        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, defaultCombination=CombinationTypes.OR), ('abc=? OR xyz=? OR test>?', ['def', 123, 42]))
        self.assertEqual(standard.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': ComparisonTypes.GREATER_THAN}}, combinations=[CombinationTypes.AND], defaultCombination=CombinationTypes.OR), ('abc=? AND xyz=? OR test>?', ['def', 123, 42]))

        self.assertEqual(standard.gen_conditions(), ('',[]))
        self.assertEqual(standard.gen_conditions({'abc':'def', 'x':'y'}, defaultCombination="OR"), ('abc=? OR x=?',['def','y']))
        self.assertEqual(standard.gen_conditions({'abc':'def', 'x':'y'}, defaultComparison=">="), ('abc>=? AND x>=?',['def','y']))
        self.assertEqual(standard.gen_conditions({'abc':'def', 'x':{'value': 'y', 'comparison': ">="}}), ('abc=? AND x>=?',['def','y']))
        self.assertEqual(standard.gen_conditions({'abc':'def', 'x':'y', 'hello': 'world'}, combinations=["OR", "AND"]), ('abc=? OR x=? AND hello=?',['def','y','world']))

    def test_A_A_b_gen_conditions(self):
        with self.assertRaises(exceptions.InvalidType):
            standard.gen_conditions(['test'])

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_conditions(combinations={})

        with self.assertRaises(exceptions.NotACombinationType):
            standard.gen_conditions(defaultCombination='abc')

        with self.assertRaises(exceptions.NotACombinationType):
            standard.gen_conditions({}, combinations=[CombinationTypes.AND, 'xyz'])

        with self.assertRaises(exceptions.NotAComparisonType):
            standard.gen_conditions(defaultComparison="abc")

        with self.assertRaises(exceptions.NotAComparisonType):
            standard.gen_conditions({'abc': {'value': 'def', 'comparison': 'xy'}})

        with self.assertRaises(exceptions.NoValue):
            standard.gen_conditions({'abc': {}})

        with self.assertRaises(exceptions.NoValue):
            standard.gen_conditions({'abc': {'comparison': ComparisonTypes.EQUAL_TO}})

    def test_A_A_c_gen_insert(self):
        self.assertEqual(standard.gen_insert("TestA", {"colA":"val1", "colB": 123, "colC": True}), ("INSERT INTO TestA (colA, colB, colC) VALUES (?, ?, ?);", ['val1', 123, True]))

    def test_A_B_gen_insert(self):
        with self.assertRaises(exceptions.DictionaryEmptyException):
            standard.gen_insert("TestB", {})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_insert(" Test B", {"colA":"val1", "colB": 123, "colC": True})

    def test_A_C_gen_insert(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_insert("", {"colA": "val1"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_insert(" ", {"colA": "val1"})

    def test_A_D_gen_delete(self):
        self.assertEqual(standard.gen_delete("TestD", {"colXY": "ABC", "id": 12345}), ("DELETE FROM TestD WHERE colXY=? AND id=?;", ['ABC', 12345]))
        self.assertEqual(standard.gen_delete("TestD", {"colXY": "ABC", "id": 12345}, conditionCombining='OR'), ("DELETE FROM TestD WHERE colXY=? OR id=?;", ['ABC', 12345]))
        self.assertEqual(standard.gen_delete("TestD"), ("DELETE FROM TestD;", []))

    def test_A_E_gen_delete(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("", {"col": "val"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("", {"col": "val"}, "OR")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete(" ")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete(" ", {"col": "val"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete(" ", {"col": "val"}, "OR")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("TestD ")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("T es tD", {"colXY": "ABC", "id": 12345})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("T es tD", {"colXY": "ABC", "id": 12345}, 'OR')

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("T es tD")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_delete("T es tD ")

    def test_A_F_gen_create_db(self):
        self.assertTrue(standard.gen_create_db("TestF"))

    def test_A_G_gen_create_db(self):
        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db("")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db(" ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db("   ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db(" Tes tF ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db(" TestF")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db("TestF ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_create_db(" Tes   tF ")

    def test_A_H_gen_create_table(self):
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int"}, safeMode=False), "CREATE TABLE TestH (col1 int);")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int"}, safeMode=True), "CREATE TABLE IF NOT EXISTS TestH (col1 int);")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int"}), "CREATE TABLE IF NOT EXISTS TestH (col1 int);")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=False), "CREATE TABLE TestH (col1 int, xyz char);")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=True), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);")

        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['col1']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (col1));")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['col1', 'xyz']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (col1,xyz));")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, foreignKeys={'col1': 'Test(Hello)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, FOREIGN KEY (col1) REFERENCES Test(Hello));")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, foreignKeys={'col1': 'Test(Hello)', 'xyz': 'Test(World)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, FOREIGN KEY (col1) REFERENCES Test(Hello), FOREIGN KEY (xyz) REFERENCES Test(World));")

        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['xyz'], foreignKeys={'col1': 'Test(Hello)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (xyz), FOREIGN KEY (col1) REFERENCES Test(Hello));")

        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, uniqueColumns=['col1']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, UNIQUE (col1));")
        self.assertEqual(standard.gen_create_table("TestH", {"col1": "int", "xyz": "char", "abc": "int"}, primaryKeys=['xyz'], foreignKeys={'col1': 'Test(Hello)'}, uniqueColumns=['abc']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, abc int, PRIMARY KEY (xyz), FOREIGN KEY (col1) REFERENCES Test(Hello), UNIQUE (abc));")

        self.assertEqual(standard.gen_create_table("TestH", {"col1": "varchar(10)"}, namedForeignKeys={"col1": {"name": "TestFK", "reference": "TableXY(abc)"}}), "CREATE TABLE IF NOT EXISTS TestH (col1 varchar(10), CONSTRAINT TestFK FOREIGN KEY (col1) REFERENCES TableXY(abc));")

    def test_A_I_gen_create_table(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table("", {"id": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table("  ", {"id": "int"})

        with self.assertRaises(exceptions.DictionaryEmptyException):
            standard.gen_create_table("TestI", {})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table("Tes t H", {"col1": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table(" T  es tH", {"col1": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table("Te stH", {"col1": "int", "xyz": "char"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_create_table("Te stH  ", {"col1": "int", "xyz": "char"})

        with self.assertRaises(exceptions.InvalidPrimaryKeyColumn):
            standard.gen_create_table("Test", {'col1': 'int'}, primaryKeys=['col2'])

        with self.assertRaises(exceptions.InvalidForeignKeyColumn):
            standard.gen_create_table("Test", {'col1': 'int'}, foreignKeys={'col2': 'Test(xyz)'})

        with self.assertRaises(exceptions.InvalidUniqueColumn):
            standard.gen_create_table("Test", {'col1': 'int'}, uniqueColumns=['col2'])

        with self.assertRaises(exceptions.InvalidForeignKeyColumn):
            standard.gen_create_table("Test", {'col1': 'int'}, namedForeignKeys={'col2': {'name':"testFK", "reference": "TableABC(def)"}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            standard.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": 42})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            standard.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            standard.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {'name': 'testFK'}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            standard.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {'reference': 'anotherTable(aColumn)'}})

    def test_A_J_INVALID_CHARS(self):
        self.assertEqual(standard.INVALID_CHARS, ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t'])

    def test_A_K_check_validName(self):
        chars = string.ascii_letters + string.digits

        for i in range(10):
            for char in standard.INVALID_CHARS:
                text = [random.choice(chars) for _ in range(random.randint(10,100))]

                text[random.randint(0, len(text)-1)] = char

                text = ''.join(text)

                self.assertFalse(standard.check_validName(text))

    def test_A_L_check_validName(self):
        chars = string.ascii_letters + string.digits

        for _ in range(50):
            text = ''.join([random.choice(chars) for _ in range(70)])

            self.assertTrue(standard.check_validName(text))

    def test_A_M_gen_update(self):
        self.assertEqual(standard.gen_update("TableA", {"col1": "val1"}), ("UPDATE TableA SET col1=?;", ['val1']))
        self.assertEqual(standard.gen_update("TableA", {"col1": True}), ("UPDATE TableA SET col1=?;", [True]))
        self.assertEqual(standard.gen_update("TableA", {"col1": 42}), ("UPDATE TableA SET col1=?;", [42]))

        self.assertEqual(standard.gen_update("TableA", {"col1": "val1"}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 'hello']))
        self.assertEqual(standard.gen_update("TableA", {"col1": "val1"}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', True]))
        self.assertEqual(standard.gen_update("TableA", {"col1": "val1"}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 42]))

        self.assertEqual(standard.gen_update("TableA", {"col1": True}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 'hello']))
        self.assertEqual(standard.gen_update("TableA", {"col1": True}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, True]))
        self.assertEqual(standard.gen_update("TableA", {"col1": True}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 42]))

        self.assertEqual(standard.gen_update("TableA", {"col1": 42}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 'hello']))
        self.assertEqual(standard.gen_update("TableA", {"col1": 42}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, True]))
        self.assertEqual(standard.gen_update("TableA", {"col1": 42}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 42]))

        self.assertEqual(standard.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}, conditionCombining="OR"), ("UPDATE TableA SET col1=? WHERE col5=? OR colB=?;", [42, 42, 'welt']))
        self.assertEqual(standard.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}), ("UPDATE TableA SET col1=? WHERE col5=? AND colB=?;", [42, 42, 'welt']))

    def test_A_N_gen_update(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_update("T abl e", {"col1": "val1"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_update("", {"col1": "val1"})

        with self.assertRaises(exceptions.DictionaryEmptyException):
            standard.gen_update("TableXY", {})

    def test_A_O_gen_drop_db(self):
        self.assertEqual(standard.gen_drop_db("DbA"), 'DROP DATABASE DbA;')

    def test_A_P_gen_drop_db(self):
        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            standard.gen_drop_db("")

    def test_A_Q_gen_drop_table(self):
        self.assertEqual(standard.gen_drop_table("TableA"), 'DROP TABLE TableA;')

    def test_A_R_gen_drop_table(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_drop_table("")

    def test_A_S_gen_select(self):
        self.assertEqual(standard.gen_select("TableS"), ('SELECT * FROM TableS;', []))
        self.assertEqual(standard.gen_select("TableS", ["col1", "xyz"]), ('SELECT col1, xyz FROM TableS;', []))
        self.assertEqual(standard.gen_select("TableS", ["xyz"]), ('SELECT xyz FROM TableS;', []))
        self.assertEqual(standard.gen_select("TableS", conditions={"col5":"hello"}), ('SELECT * FROM TableS WHERE col5=?;', ['hello']))
        self.assertEqual(standard.gen_select("TableS", ["abc", "def"], conditions={"col5":"hello"}), ('SELECT abc, def FROM TableS WHERE col5=?;', ['hello']))
        self.assertEqual(standard.gen_select("TableS", conditions={"col5":"hello", "xyz": "abc"}), ('SELECT * FROM TableS WHERE col5=? AND xyz=?;', ['hello', 'abc']))
        self.assertEqual(standard.gen_select("TableS", ["abc", "def"], conditions={"col5":"hello", "xyz": "abc"}), ('SELECT abc, def FROM TableS WHERE col5=? AND xyz=?;', ['hello', 'abc']))

        self.assertEqual(standard.gen_select("TableS", ["abc", "def"], conditions={"col5":"hello"}, distinct=True), ('SELECT DISTINCT abc, def FROM TableS WHERE col5=?;', ['hello']))

    def test_A_T_gen_select(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_select("")

    def test_A_U_gen_count_avg_sum(self):
        with self.assertRaises(exceptions.InvalidType):
            standard.gen_count_avg_sum(None, "TableA", "ColumnB")

        with self.assertRaises(exceptions.InvalidTableNameException):
            standard.gen_count_avg_sum(standard.Count_avg_sum_modes.COUNT, "", "ColumnB")

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_count_avg_sum(standard.Count_avg_sum_modes.COUNT, "TableA", None)

    def test_A_V_gen_count(self):
        self.assertEqual(standard.gen_count("TableA"), ("SELECT COUNT(*) FROM TableA;", []))
        self.assertEqual(standard.gen_count("TableA", "myColumn"), ("SELECT COUNT(myColumn) FROM TableA;", []))
        self.assertEqual(standard.gen_count("TableA", "myColumn", {"colB": 123}), ("SELECT COUNT(myColumn) FROM TableA WHERE colB=?;", [123]))

        self.assertEqual(standard.gen_count("TableA", "myColumn", {"colB": 123}, distinct=True), ("SELECT COUNT(DISTINCT myColumn) FROM TableA WHERE colB=?;", [123]))

    def test_A_W_gen_avg(self):
        self.assertEqual(standard.gen_avg("TableA"), ("SELECT AVG(*) FROM TableA;", []))
        self.assertEqual(standard.gen_avg("TableA", "myColumn"), ("SELECT AVG(myColumn) FROM TableA;", []))
        self.assertEqual(standard.gen_avg("TableA", "myColumn", {"colB": 123}), ("SELECT AVG(myColumn) FROM TableA WHERE colB=?;", [123]))

        self.assertEqual(standard.gen_avg("TableA", "myColumn", {"colB": 123}, distinct=True), ("SELECT AVG(DISTINCT myColumn) FROM TableA WHERE colB=?;", [123]))

    def test_A_X_gen_sum(self):
        self.assertEqual(standard.gen_sum("TableA"), ("SELECT SUM(*) FROM TableA;", []))
        self.assertEqual(standard.gen_sum("TableA", "myColumn"), ("SELECT SUM(myColumn) FROM TableA;", []))
        self.assertEqual(standard.gen_sum("TableA", "myColumn", {"colB": 123}), ("SELECT SUM(myColumn) FROM TableA WHERE colB=?;", [123]))

        self.assertEqual(standard.gen_sum("TableA", "myColumn", {"colB": 123}, distinct=True), ("SELECT SUM(DISTINCT myColumn) FROM TableA WHERE colB=?;", [123]))

    def test_A_Y_a_gen_create_stored_procedure(self):
        self.assertEqual(standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;"), "CREATE PROCEDURE Test\nAS\nSELECT * FROM TableA;\nGO;")
        self.assertEqual(standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", {'param': 'varchar(10)'}), "CREATE PROCEDURE Test @param varchar(10)\nAS\nSELECT * FROM TableA;\nGO;")
        self.assertEqual(standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", {'param': 'varchar(10)', 'param2': 'varchar(20)'}), "CREATE PROCEDURE Test @param varchar(10), @param2 varchar(20)\nAS\nSELECT * FROM TableA;\nGO;")

    def test_A_Y_b_gen_create_stored_procedure(self):
        with self.assertRaises(exceptions.InvalidType):
            standard.gen_create_stored_procedure(123, "SELECT * FROM TableA;")

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_create_stored_procedure("Test", 456)

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", ['abc','def'])

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", {123:'456'})

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", {'123':456})

    def test_A_Z_a_gen_exec_procedure(self):
        self.assertEqual(standard.gen_exec_procedure("Test"), ("EXEC Test;", []))
        self.assertEqual(standard.gen_exec_procedure("Test", {'param': 'val1'}), ("EXEC Test @param=?;", ['val1']))
        self.assertEqual(standard.gen_exec_procedure("Test", {'param': 'val1', 'param2': 'val2'}), ("EXEC Test @param=?, @param2=?;", ['val1', 'val2']))

    def test_A_Z_b_gen_exec_procedure(self):
        with self.assertRaises(exceptions.InvalidType):
            standard.gen_exec_procedure(123)

        with self.assertRaises(exceptions.InvalidType):
            standard.gen_exec_procedure("Test", ['abc','def'])

    def test_B_A_b_gen_drop_procedure(self):
        self.assertEqual(standard.gen_drop_procedure("Test"), "DROP PROCEDURE Test;")

    def test_B_A_b_gen_drop_procedure(self):
        with self.assertRaises(exceptions.InvalidType):
            standard.gen_drop_procedure(123)

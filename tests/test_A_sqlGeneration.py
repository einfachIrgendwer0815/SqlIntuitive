from sqlIntuitive import sqlGeneration, exceptions

import unittest

import random, string

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqlGeneration = json.load(file)['sqlGeneration']

@unittest.skipIf(runTestSqlGeneration == False, 'Skipped TestSqlGeneration via config')
class TestSqlGeneration(unittest.TestCase):
    def test_A_a_gen_conditions(self):
        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}), ('abc=? AND xyz=? AND test>?', ['def', 123, 42]))
        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, defaultComparison=sqlGeneration.ComparisonTypes.LESS_THAN_OR_EQUAL_TO), ('abc<=? AND xyz<=? AND test>?', ['def', 123, 42]))
        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, defaultCombination=sqlGeneration.CombinationTypes.OR), ('abc=? OR xyz=? OR test>?', ['def', 123, 42]))

        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, combinations=[sqlGeneration.CombinationTypes.OR]), ('abc=? OR xyz=? AND test>?', ['def', 123, 42]))
        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, combinations=[sqlGeneration.CombinationTypes.OR, sqlGeneration.CombinationTypes.AND, sqlGeneration.CombinationTypes.OR]), ('abc=? OR xyz=? AND test>?', ['def', 123, 42]))

        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, defaultCombination=sqlGeneration.CombinationTypes.OR), ('abc=? OR xyz=? OR test>?', ['def', 123, 42]))
        self.assertEqual(sqlGeneration.gen_conditions({'abc': 'def', 'xyz': {'value': 123}, 'test': {'value': 42, 'comparison': sqlGeneration.ComparisonTypes.GREATER_THAN}}, combinations=[sqlGeneration.CombinationTypes.AND], defaultCombination=sqlGeneration.CombinationTypes.OR), ('abc=? AND xyz=? OR test>?', ['def', 123, 42]))

        self.assertEqual(sqlGeneration.gen_conditions(), ('',[]))
        self.assertEqual(sqlGeneration.gen_conditions({'abc':'def', 'x':'y'}, defaultCombination="OR"), ('abc=? OR x=?',['def','y']))
        self.assertEqual(sqlGeneration.gen_conditions({'abc':'def', 'x':'y'}, defaultComparison=">="), ('abc>=? AND x>=?',['def','y']))
        self.assertEqual(sqlGeneration.gen_conditions({'abc':'def', 'x':{'value': 'y', 'comparison': ">="}}), ('abc=? AND x>=?',['def','y']))
        self.assertEqual(sqlGeneration.gen_conditions({'abc':'def', 'x':'y', 'hello': 'world'}, combinations=["OR", "AND"]), ('abc=? OR x=? AND hello=?',['def','y','world']))

    def test_A_b_gen_conditions(self):
        with self.assertRaises(exceptions.InvalidType):
            sqlGeneration.gen_conditions(['test'])

        with self.assertRaises(exceptions.InvalidType):
            sqlGeneration.gen_conditions(combinations={})

        with self.assertRaises(exceptions.NotACombinationType):
            sqlGeneration.gen_conditions(defaultCombination='abc')

        with self.assertRaises(exceptions.NotACombinationType):
            sqlGeneration.gen_conditions({}, combinations=[sqlGeneration.CombinationTypes.AND, 'xyz'])

        with self.assertRaises(exceptions.NotAComparisonType):
            sqlGeneration.gen_conditions(defaultComparison="abc")

        with self.assertRaises(exceptions.NotAComparisonType):
            sqlGeneration.gen_conditions({'abc': {'value': 'def', 'comparison': 'xy'}})

        with self.assertRaises(exceptions.NoValue):
            sqlGeneration.gen_conditions({'abc': {}})

        with self.assertRaises(exceptions.NoValue):
            sqlGeneration.gen_conditions({'abc': {'comparison': sqlGeneration.ComparisonTypes.EQUAL_TO}})

    def test_A_b_gen_insert(self):
        self.assertEqual(sqlGeneration.gen_insert("TestA", {"colA":"val1", "colB": 123, "colC": True}), ("INSERT INTO TestA (colA, colB, colC) VALUES (?, ?, ?);", ['val1', 123, True]))

    def test_B_gen_insert(self):
        with self.assertRaises(exceptions.DictionaryEmptyException):
            sqlGeneration.gen_insert("TestB", {})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_insert(" Test B", {"colA":"val1", "colB": 123, "colC": True})

    def test_C_gen_insert(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_insert("", {"colA": "val1"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_insert(" ", {"colA": "val1"})

    def test_D_gen_delete(self):
        self.assertEqual(sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}), ("DELETE FROM TestD WHERE colXY=? AND id=?;", ['ABC', 12345]))
        self.assertEqual(sqlGeneration.gen_delete("TestD", {"colXY": "ABC", "id": 12345}, conditionCombining='OR'), ("DELETE FROM TestD WHERE colXY=? OR id=?;", ['ABC', 12345]))
        self.assertEqual(sqlGeneration.gen_delete("TestD"), ("DELETE FROM TestD;", []))

    def test_E_gen_delete(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("", {"col": "val"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("", {"col": "val"}, "OR")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete(" ")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete(" ", {"col": "val"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete(" ", {"col": "val"}, "OR")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("TestD ")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("T es tD", {"colXY": "ABC", "id": 12345}, 'OR')

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("T es tD")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_delete("T es tD ")

    def test_F_gen_create_db(self):
        self.assertTrue(sqlGeneration.gen_create_db("TestF"))

    def test_G_gen_create_db(self):
        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db("")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db(" ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db("   ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db(" Tes tF ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db(" TestF")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db("TestF ")

        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_create_db(" Tes   tF ")

    def test_H_gen_create_table(self):
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int"}, safeMode=False), "CREATE TABLE TestH (col1 int);")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int"}, safeMode=True), "CREATE TABLE IF NOT EXISTS TestH (col1 int);")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int"}), "CREATE TABLE IF NOT EXISTS TestH (col1 int);")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=False), "CREATE TABLE TestH (col1 int, xyz char);")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, safeMode=True), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char);")

        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['col1']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (col1));")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['col1', 'xyz']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (col1,xyz));")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, foreignKeys={'col1': 'Test(Hello)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, FOREIGN KEY (col1) REFERENCES Test(Hello));")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, foreignKeys={'col1': 'Test(Hello)', 'xyz': 'Test(World)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, FOREIGN KEY (col1) REFERENCES Test(Hello), FOREIGN KEY (xyz) REFERENCES Test(World));")

        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, primaryKeys=['xyz'], foreignKeys={'col1': 'Test(Hello)'}), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, PRIMARY KEY (xyz), FOREIGN KEY (col1) REFERENCES Test(Hello));")

        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char"}, uniqueColumns=['col1']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, UNIQUE (col1));")
        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "int", "xyz": "char", "abc": "int"}, primaryKeys=['xyz'], foreignKeys={'col1': 'Test(Hello)'}, uniqueColumns=['abc']), "CREATE TABLE IF NOT EXISTS TestH (col1 int, xyz char, abc int, PRIMARY KEY (xyz), FOREIGN KEY (col1) REFERENCES Test(Hello), UNIQUE (abc));")

        self.assertEqual(sqlGeneration.gen_create_table("TestH", {"col1": "varchar(10)"}, namedForeignKeys={"col1": {"name": "TestFK", "reference": "TableXY(abc)"}}), "CREATE TABLE IF NOT EXISTS TestH (col1 varchar(10), CONSTRAINT TestFK FOREIGN KEY (col1) REFERENCES TableXY(abc));")

    def test_I_gen_create_table(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table("", {"id": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table("  ", {"id": "int"})

        with self.assertRaises(exceptions.DictionaryEmptyException):
            sqlGeneration.gen_create_table("TestI", {})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table("Tes t H", {"col1": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table(" T  es tH", {"col1": "int"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table("Te stH", {"col1": "int", "xyz": "char"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_create_table("Te stH  ", {"col1": "int", "xyz": "char"})

        with self.assertRaises(exceptions.InvalidPrimaryKeyColumn):
            sqlGeneration.gen_create_table("Test", {'col1': 'int'}, primaryKeys=['col2'])

        with self.assertRaises(exceptions.InvalidForeignKeyColumn):
            sqlGeneration.gen_create_table("Test", {'col1': 'int'}, foreignKeys={'col2': 'Test(xyz)'})

        with self.assertRaises(exceptions.InvalidUniqueColumn):
            sqlGeneration.gen_create_table("Test", {'col1': 'int'}, uniqueColumns=['col2'])

        with self.assertRaises(exceptions.InvalidForeignKeyColumn):
            sqlGeneration.gen_create_table("Test", {'col1': 'int'}, namedForeignKeys={'col2': {'name':"testFK", "reference": "TableABC(def)"}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            sqlGeneration.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": 42})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            sqlGeneration.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            sqlGeneration.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {'name': 'testFK'}})

        with self.assertRaises(exceptions.InvalidNamedForeignKeyDictionary):
            sqlGeneration.gen_create_table("Test", {"col1": "int"}, namedForeignKeys={"col1": {'reference': 'anotherTable(aColumn)'}})

    def test_J_INVALID_CHARS(self):
        self.assertEqual(sqlGeneration.INVALID_CHARS, ['!', '"', '#', r'\$', '%', '&', "'", r'\(', r'\)', r'\*', r'\+', ',', '-', '/', ':', ';', '<', '=', '>', r'\?', '@', r'\[', r'\\', r'\]', r'\^', '_', '`', r'\{', r'\|', r'\}', '~', ' ', '\n', '\t'])

    def test_K_check_validName(self):
        chars = string.ascii_letters + string.digits

        for i in range(10):
            for char in sqlGeneration.INVALID_CHARS:
                text = [random.choice(chars) for _ in range(random.randint(10,100))]

                text[random.randint(0, len(text)-1)] = char

                text = ''.join(text)

                self.assertFalse(sqlGeneration.check_validName(text))

    def test_L_check_validName(self):
        chars = string.ascii_letters + string.digits

        for _ in range(50):
            text = ''.join([random.choice(chars) for _ in range(70)])

            self.assertTrue(sqlGeneration.check_validName(text))

    def test_M_gen_update(self):
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": "val1"}), ("UPDATE TableA SET col1=?;", ['val1']))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": True}), ("UPDATE TableA SET col1=?;", [True]))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}), ("UPDATE TableA SET col1=?;", [42]))

        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 'hello']))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', True]))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": "val1"}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", ['val1', 42]))

        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 'hello']))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, True]))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": True}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", [True, 42]))

        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 'hello'}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 'hello']))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': True}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, True]))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42}), ("UPDATE TableA SET col1=? WHERE col5=?;", [42, 42]))

        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}, conditionCombining="OR"), ("UPDATE TableA SET col1=? WHERE col5=? OR colB=?;", [42, 42, 'welt']))
        self.assertEqual(sqlGeneration.gen_update("TableA", {"col1": 42}, {'col5': 42, "colB": "welt"}), ("UPDATE TableA SET col1=? WHERE col5=? AND colB=?;", [42, 42, 'welt']))

    def test_N_gen_update(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_update("T abl e", {"col1": "val1"})

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_update("", {"col1": "val1"})

        with self.assertRaises(exceptions.DictionaryEmptyException):
            sqlGeneration.gen_update("TableXY", {})

    def test_O_gen_drop_db(self):
        self.assertEqual(sqlGeneration.gen_drop_db("DbA"), 'DROP DATABASE DbA;')

    def test_P_gen_drop_db(self):
        with self.assertRaises(exceptions.InvalidDatabaseNameException):
            sqlGeneration.gen_drop_db("")

    def test_Q_gen_drop_table(self):
        self.assertEqual(sqlGeneration.gen_drop_table("TableA"), 'DROP TABLE TableA;')

    def test_R_gen_drop_table(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_drop_table("")

    def test_S_gen_select(self):
        self.assertEqual(sqlGeneration.gen_select("TableS"), ('SELECT * FROM TableS;', []))
        self.assertEqual(sqlGeneration.gen_select("TableS", ["col1", "xyz"]), ('SELECT col1, xyz FROM TableS;', []))
        self.assertEqual(sqlGeneration.gen_select("TableS", ["xyz"]), ('SELECT xyz FROM TableS;', []))
        self.assertEqual(sqlGeneration.gen_select("TableS", conditions={"col5":"hello"}), ('SELECT * FROM TableS WHERE col5=?;', ['hello']))
        self.assertEqual(sqlGeneration.gen_select("TableS", ["abc", "def"], conditions={"col5":"hello"}), ('SELECT abc, def FROM TableS WHERE col5=?;', ['hello']))
        self.assertEqual(sqlGeneration.gen_select("TableS", conditions={"col5":"hello", "xyz": "abc"}), ('SELECT * FROM TableS WHERE col5=? AND xyz=?;', ['hello', 'abc']))
        self.assertEqual(sqlGeneration.gen_select("TableS", ["abc", "def"], conditions={"col5":"hello", "xyz": "abc"}), ('SELECT abc, def FROM TableS WHERE col5=? AND xyz=?;', ['hello', 'abc']))

    def test_T_gen_select(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlGeneration.gen_select("")

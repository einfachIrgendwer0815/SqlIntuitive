from sqlIntuitive import exceptions
from sqlIntuitive.sqlGeneration import sqlite

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqlGenerationSqlite = json.load(file)['sqlGeneration_sqlite']

@unittest.skipIf(runTestSqlGenerationSqlite == False, 'Skipped TestSqlGenerationSqlite via config')
class TestSqlGenerationSqlite(unittest.TestCase):
    def test_A_gen_alter_table_rename_table(self):
        self.assertEqual(sqlite.gen_alter_table_rename_table("TableA","TableB"), "ALTER TABLE TableA RENAME TO TableB;")

    def test_B_gen_alter_table_rename_table(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_table("!%&/()", "TableB")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_table("", "TableB")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_table("TableA", "!%&/()")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_table("TableA", "")

    def test_C_gen_alter_table_rename_column(self):
        self.assertEqual(sqlite.gen_alter_table_rename_column("TableA", "col1", "colABC"), "ALTER TABLE TableA RENAME COLUMN col1 TO colABC;")

    def test_D_gen_alter_table_rename_column(self):
        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_column("!%&/()", "col1", "colABC")

        with self.assertRaises(exceptions.InvalidTableNameException):
            sqlite.gen_alter_table_rename_column("", "col1", "colABC")

from sqlIntuitive import dbSystems
from sqlIntuitive.ext import customDataTypes

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

        cursor.execute("CREATE TABLE IF NOT EXISTS TableA (col1 int, col2 string, col3 bool, PRIMARY KEY (col1), UNIQUE (col2));")

        cursor.close()
        file_db.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(dbFile)

    def setUp(self):
        self.memory_db = dbSystems.SqliteDbSystem(database=":memory:")
        self.file_db = dbSystems.SqliteDbSystem(database=dbFile)

    def tearDown(self):
        self.memory_db.close_connection()
        self.file_db.close_connection()

    def test_A_connect_to_db(self):
        self.memory_db.connect_to_db()

        self.assertIsNotNone(self.memory_db.dbCon)

    def test_B_cursor(self):
        self.memory_db.connect_to_db()

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

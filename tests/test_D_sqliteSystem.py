from sqlIntuitive import dbSystems
from sqlIntuitive.ext import customDataTypes

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqliteSystem = json.load(file)['sqliteSystem']

@unittest.skipIf(runTestSqliteSystem == False, 'Skipped TestSqliteSystem via config')
class TestSqliteSystem(unittest.TestCase):
    def setUp(self):
        self.mydb = dbSystems.SqliteDbSystem(database=":memory:")

    def tearDown(self):
        self.mydb.close_connection()

    def test_A_connect_to_db(self):
        self.mydb.connect_to_db()

        self.assertIsNotNone(self.mydb.dbCon)

    def test_B_cursor(self):
        self.mydb.connect_to_db()

        self.assertIsNone(self.mydb.cursor)

        self.mydb.create_cursor()

        self.assertIsNotNone(self.mydb.cursor)

    def test_C_adaptionProvider(self):
        self.assertTrue(isinstance(self.mydb.adaptProvider, customDataTypes.AdaptionProvider))

        adaptProvider = customDataTypes.AdaptionProvider()
        mydb2 = dbSystems.SqliteDbSystem(":memory:", adaptionProvider=adaptProvider)

        self.assertEqual(mydb2.adaptProvider, adaptProvider)

    def test_D_open_close(self):
        self.mydb.create_cursor() # Won't work but no error is raised

        self.mydb.connect_to_db()
        self.mydb.create_cursor()
        self.mydb.close_connection()

        self.mydb.create_cursor() # Won't work too but still no error is raised

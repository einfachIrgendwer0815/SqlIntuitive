from sqlIntuitive import dbSystems

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
    

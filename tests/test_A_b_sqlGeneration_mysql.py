from sqlIntuitive import exceptions
from sqlIntuitive.sqlGeneration import mysql

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSqlGenerationMySQL = json.load(file)['sqlGeneration_mysql']

@unittest.skipIf(runTestSqlGenerationMySQL == False, 'Skipped TestSqlGenerationMySQL via config')
class TestSqlGenerationMySQL(unittest.TestCase):
    def test_A_a_gen_create_stored_procedure(self):
        self.assertEqual(mysql.gen_create_stored_procedure("TestProc", "SELECT * FROM TableA;", "$$"), "DELIMITER $$\nCREATE PROCEDURE TestProc ()\nBEGIN\nSELECT * FROM TableA;\nEND$$\nDELIMITER ;")
        self.assertEqual(mysql.gen_create_stored_procedure("TestProc", "SELECT * FROM TableA;", "$$", {'param1': 'varchar(10)'}), "DELIMITER $$\nCREATE PROCEDURE TestProc (IN param1 varchar(10))\nBEGIN\nSELECT * FROM TableA;\nEND$$\nDELIMITER ;")
        self.assertEqual(mysql.gen_create_stored_procedure("TestProc", "SELECT * FROM TableA;", "$$", {'param1': 'varchar(10)', 'param2': 'int'}), "DELIMITER $$\nCREATE PROCEDURE TestProc (IN param1 varchar(10), IN param2 int)\nBEGIN\nSELECT * FROM TableA;\nEND$$\nDELIMITER ;")

    def test_A_b_gen_create_stored_procedure(self):
        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure(123, "SELECT * FROM TableA;", "$$")

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure("Test", 456, "$$")

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", 123)

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", "$$", ['abc','def'])

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", "$$", {123:'456'})

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_create_stored_procedure("Test", "SELECT * FROM TableA;", "$$", {'123':456})

    def test_B_a_gen_exec_procedure(self):
        self.assertEqual(mysql.gen_exec_procedure("TestProc"), ("CALL TestProc ();", []))
        self.assertEqual(mysql.gen_exec_procedure("TestProc", ['2022-01-04']), ("CALL TestProc (?);", ['2022-01-04']))
        self.assertEqual(mysql.gen_exec_procedure("TestProc", ['2022-01-04',123,'HelloWorld!']), ("CALL TestProc (?, ?, ?);", ['2022-01-04',123,'HelloWorld!']))

    def test_B_b_gen_exec_procedure(self):
        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_exec_procedure(123)

        with self.assertRaises(exceptions.InvalidType):
            mysql.gen_exec_procedure("Test", ('abc','def'))

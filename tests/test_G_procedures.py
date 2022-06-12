from sqlIntuitive import exceptions
from sqlIntuitive.ext.procedures import Procedure
from sqlIntuitive import dbSystems
from sqlIntuitive.dbSystems.supportTracker import or_values, Features
from sqlIntuitive.sqlGeneration import functionEnums

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestProcedures = json.load(file)['procedures']

@unittest.skipIf(runTestProcedures == False, 'Skipped TestProcedures via config')
class TestProcedures(unittest.TestCase):
    def test_A_empty_procedure(self):
        p = Procedure()

        self.assertEqual(len(p), 0)

    def test_B_constructor(self):
        p = Procedure([
            {
                "operation": functionEnums.Standard.SELECT_FROM,
                "args": [],
                "kwargs": {
                    "tableName": "TableA",
                    "columns": ["col1", "col2"]
                }
            },
            {
                "operation": functionEnums.Standard.DELETE_FROM,
                "args": ["tableA"],
                "kwargs": {}
            }
        ])

        self.assertEqual(len(p), 2)

    def test_C_append(self):
        p = Procedure()

        c1 = {
            "operation": functionEnums.Standard.SELECT_FROM,
            "args": [],
            "kwargs": {
                "tableName": "TableA",
                "columns": ["col1", "col2"]
            }
        }
        c2 = {
            "operation": functionEnums.Standard.DELETE_FROM,
            "args": ["tableA"],
            "kwargs": {}
        }
        c3 = {
            "operation": functionEnums.Standard.SELECT_COUNT,
            "args": [],
            "kwargs": {
                "tableName": "TableA"
            }
        }

        p.append(c1)
        p.append(c2)
        p.append(c3)

        self.assertEqual(len(p), 3)
        self.assertEqual(p.commands, [c1, c2, c3])

    def test_D_insert(self):
        p = Procedure()

        c1 = {
            "operation": functionEnums.Standard.SELECT_FROM,
            "args": [],
            "kwargs": {
                "tableName": "TableA",
                "columns": ["col1", "col2"]
            }
        }
        c2 = {
            "operation": functionEnums.Standard.DELETE_FROM,
            "args": ["tableA"],
            "kwargs": {}
        }
        c3 = {
            "operation": functionEnums.Standard.SELECT_COUNT,
            "args": [],
            "kwargs": {
                "tableName": "TableA"
            }
        }

        p.append(c1)
        p.append(c2)

        p.insert(1, c3)

        self.assertEqual(len(p), 3)
        self.assertEqual(p.commands, [c1, c3, c2])

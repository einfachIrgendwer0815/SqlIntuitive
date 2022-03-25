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
        self.assertEqual(p.getFeaturesUsed(), 0)

    @unittest.skip
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
        self.assertEqual(p.getFeaturesUsed(), or_values([Features.SQL_SELECT_FROM, Features.SQL_DELETE_FROM]))

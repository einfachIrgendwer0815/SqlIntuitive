from sqlIntuitive.dbSystems import supportTracker

import unittest
import os, json

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestSupportTracker = json.load(file)['supportTracker']

@unittest.skipIf(runTestSupportTracker == False, 'Skipped TestSupportTracker via config')
class TestSupportTracker(unittest.TestCase):
    def connect_by_OR(self, numbers):
        sum = 0
        for number in numbers:
            sum = sum | number

        return sum

    def test_A_Features(self):
        featuresClassDict = supportTracker.Features.__dict__

        sqlFeatures = [featuresClassDict[i].value for i in featuresClassDict if i.startswith("SQL_")]
        addonFeatures = [featuresClassDict[i].value for i in featuresClassDict if i.startswith("ADDON_")]
        featureGroups = [featuresClassDict[i].value for i in featuresClassDict if i.startswith("GROUP_")]

        self.assertEqual(supportTracker.Features.GROUP_SQL.value, self.connect_by_OR(sqlFeatures))
        self.assertEqual(supportTracker.Features.GROUP_ADDON.value, self.connect_by_OR(addonFeatures))

        self.assertEqual(supportTracker.Features.ALL.value, self.connect_by_OR(featureGroups))

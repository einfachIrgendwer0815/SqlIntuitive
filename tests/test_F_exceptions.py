from sqlIntuitive import exceptions

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestExceptions = json.load(file)['exceptions']

@unittest.skipIf(runTestExceptions == False, 'Skipped TestExceptions via config')
class TestExceptions(unittest.TestCase):
    def test_A_staticExceptionMessages(self):
        with self.assertRaisesRegex(exceptions.SqlIntuitiveException, 'An overall exception was raised inside the modul \'sqlIntuitive\'.'):
            raise exceptions.SqlIntuitiveException()

        with self.assertRaisesRegex(exceptions.AdaptionProviderException, 'An overall exception was raised inside the class \'sqlIntuitive.ext.customDataTypes.AdaptionProvider\'.'):
            raise exceptions.AdaptionProviderException()

        with self.assertRaisesRegex(exceptions.ConditionException, 'An overall \'Condition exception\' was raised processing a condition.'):
            raise exceptions.ConditionException()

    def test_B_adaptionProviderExceptions(self):
        with self.assertRaisesRegex(exceptions.DuplicationError, '.* (.*) are already registered'):
            raise exceptions.DuplicationError("TEST", 123)

        with self.assertRaisesRegex(exceptions.DeletingTypeNotAllowed, r'It is not allowed to remove .*\.'):
            raise exceptions.DeletingTypeNotAllowed("TEST")

    def test_C_conditionExceptions(self):
        with self.assertRaisesRegex(exceptions.NotAComparisonType, r'.* is not a comparison type\.'):
            raise exceptions.NotAComparisonType(type(123))

        with self.assertRaisesRegex(exceptions.NotACombinationType, r'.* is not a combination type\.'):
            raise exceptions.NotACombinationType(type(123))

        with self.assertRaisesRegex(exceptions.NoValue, r'No value for .*\.'):
            raise exceptions.NoValue("abc")

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

        with self.assertRaisesRegex(exceptions.ParameterException, 'An overall \'Parameter exception\' was raised.'):
            raise exceptions.ParameterException()

        with self.assertRaisesRegex(exceptions.InvalidConstraint, 'An overall \'Invalid constraint\' parameter exception was raised.'):
            raise exceptions.InvalidConstraint()

        with self.assertRaisesRegex(exceptions.InvalidTableNameException, 'Name for table contains invalid characters or is empty.'):
            raise exceptions.InvalidTableNameException()

        with self.assertRaisesRegex(exceptions.InvalidDatabaseNameException, 'Name for database contains invalid characters or is empty.'):
            raise exceptions.InvalidDatabaseNameException()

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

    def test_D_parameterExceptions(self):
        with self.assertRaisesRegex(exceptions.InvalidType, r'\'.*\' is not an instance of .*\.'):
            raise exceptions.InvalidType("abc", int)

        with self.assertRaisesRegex(exceptions.DictionaryEmptyException, 'Text'):
            raise exceptions.DictionaryEmptyException("Text")

    def test_E_invalidConstraints(self):
        with self.assertRaisesRegex(exceptions.InvalidPrimaryKeyColumn, r'.* not in columns\.'):
            raise exceptions.InvalidPrimaryKeyColumn("abc")

        with self.assertRaisesRegex(exceptions.InvalidForeignKeyColumn, r'.* not in columns\.'):
            raise exceptions.InvalidForeignKeyColumn("abc")

        with self.assertRaisesRegex(exceptions.InvalidUniqueColumn, r'.* not in columns\.'):
            raise exceptions.InvalidUniqueColumn("abc")

        with self.assertRaisesRegex(exceptions.InvalidNamedForeignKeyDictionary, r'Values for column .* are not defined\.'):
            raise exceptions.InvalidNamedForeignKeyDictionary("abc")

        with self.assertRaisesRegex(exceptions.NotAClass, r'.* is not a class\.'):
            raise exceptions.NotAClass("abc")

        with self.assertRaisesRegex(exceptions.NotAFunction, r'.* is not a function\.'):
            raise exceptions.NotAFunction("abc")

        with self.assertRaisesRegex(exceptions.NotAString, r'.* is not a string\.'):
            raise exceptions.NotAString("abc")

        with self.assertRaisesRegex(exceptions.NotAMatchingClass, r'.* does not match .*\.'):
            raise exceptions.NotAMatchingClass(int, str)

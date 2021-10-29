from sqlIntuitive.ext import customDataTypes
from sqlIntuitive import exceptions, conditionEnums

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestCustomDataTypes = json.load(file)['customDataTypes']

@unittest.skipIf(runTestCustomDataTypes == False, 'Skipped TestDBSystems via config')
class TestcustomDataTypes(unittest.TestCase):
    def setUpClass():
        cls = TestcustomDataTypes

        class Test():
            pass

        def clsToString(clsInstance):
            return str(clsInstance)

        def stringToCls(string):
            return Test()

        cls.Test = Test
        cls.clsToString = clsToString
        cls.stringToCls = stringToCls

        class TestB():
            def __init__(self, num):
                self.num = num

        def testBToString(instance):
            return str(instance.num)

        def stringToTestB(string):
            return TestB(int(string))

        cls.TestB = TestB
        cls.testBToString = testBToString
        cls.stringToTestB = stringToTestB

        class MyClass():
            def __init__(self, arg):
                self.arg = arg

        def myClassToString(clsInstance):
            return str(clsInstance.arg)

        def stringToMyClass(string):
            return MyClass(string)

        cls.MyClass = MyClass
        cls.myClassToString = myClassToString
        cls.stringToMyClass = stringToMyClass

    def test_A_customDataType_init(self):
        customType = customDataTypes.CustomDataType("Test", TestcustomDataTypes.Test, TestcustomDataTypes.clsToString, TestcustomDataTypes.stringToCls)

        self.assertEqual(customType.name, "TEST")

    def test_B_customDataType_convertToString(self):
        customType = customDataTypes.CustomDataType("Test", TestcustomDataTypes.TestB, TestcustomDataTypes.testBToString, TestcustomDataTypes.stringToTestB)

        self.assertEqual(customType.convertToString( TestcustomDataTypes.TestB(123) ), "CUSTOM;TEST;MTIz")

        instance = customType.convertToClsInstance("CUSTOM;TEST;MTIz")
        self.assertTrue(isinstance(instance, TestcustomDataTypes.TestB))
        self.assertEqual(instance.num, 123)

    def test_C_adaptionProvider_normalValues(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        self.assertEqual(adaptProvider.convertToString('this is a test string'), 'this is a test string')
        self.assertEqual(adaptProvider.convertToClsInstance('this is a test string'), 'this is a test string')

        self.assertEqual(adaptProvider.convertToString(123), 123)
        self.assertEqual(adaptProvider.convertToClsInstance(123), 123)

    def test_D_adaptionProvider_str_encoded(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        self.assertEqual(adaptProvider.convertToString("CUSTOM;4v67q8936mnpq2"), "CUSTOM;STR_ENCODED;Q1VTVE9NOzR2NjdxODkzNm1ucHEy")
        self.assertEqual(adaptProvider.convertToClsInstance("CUSTOM;STR_ENCODED;Q1VTVE9NOzR2NjdxODkzNm1ucHEy"), "CUSTOM;4v67q8936mnpq2")

    def test_E_adaptionProvider_customType(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        adaptProvider.addDataType(dataType)

        self.assertEqual(adaptProvider.convertToString(TestcustomDataTypes.MyClass("abc")), "CUSTOM;MYCLS;YWJj")

        clsInstance = adaptProvider.convertToClsInstance("CUSTOM;MYCLS;YWJj")
        self.assertEqual(type(clsInstance), TestcustomDataTypes.MyClass)
        self.assertEqual(clsInstance.arg, "abc")

    def test_F_adaptionProvicer_raw_add(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        adaptProvider.addDataType_raw("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)

        self.assertTrue("MYCLS" in adaptProvider.types)

    def test_G_adaptionProvider_removeDataType(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        adaptProvider.addDataType(dataType)

        self.assertTrue("MYCLS" in adaptProvider.types)

        adaptProvider.removeDataType(dataType.name)

        self.assertFalse("MYCLS" in adaptProvider.types, {})

    def test_H_customDataType_error_test(self):
        with self.assertRaises(exceptions.NotAString):
            dataType = customDataTypes.CustomDataType(123, TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)

        with self.assertRaises(exceptions.NotAClass):
            dataType = customDataTypes.CustomDataType("MYCLS", "abc", TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)

        with self.assertRaises(exceptions.NotAFunction):
            dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, None, TestcustomDataTypes.stringToMyClass)

        with self.assertRaises(exceptions.NotAFunction):
            dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, None)

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        with self.assertRaises(exceptions.NotAMatchingClass):
            dataType.convertToString(TestcustomDataTypes.TestB(123))

        def wrongConvertToString(clsInstance):
            return clsInstance

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, wrongConvertToString, TestcustomDataTypes.stringToMyClass)
        with self.assertRaises(exceptions.NotAString):
            dataType.convertToString(TestcustomDataTypes.MyClass(123))

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        with self.assertRaises(exceptions.NotAString):
            dataType.convertToClsInstance(123)

        def wrongConvertToClsInstance(string):
            return string

        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, wrongConvertToClsInstance)
        with self.assertRaises(exceptions.NotAMatchingClass):
            dataType.convertToClsInstance("CUSTOM;MYCLS;MTIz")

    def test_I_adaptionProvider_error_test(self):
        adaptProvider = customDataTypes.AdaptionProvider()
        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        dataType2 = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)
        adaptProvider.addDataType(dataType)

        with self.assertRaises(exceptions.DuplicationError):
            adaptProvider.addDataType(dataType2)

        adaptProvider = customDataTypes.AdaptionProvider()
        with self.assertRaises(exceptions.NotAString):
            adaptProvider.removeDataType(123)

        adaptProvider = customDataTypes.AdaptionProvider()
        with self.assertRaises(exceptions.DeletingTypeNotAllowed):
            adaptProvider.removeDataType("STR_ENCODED")

        adaptProvider = customDataTypes.AdaptionProvider()
        with self.assertRaises(KeyError):
            adaptProvider.removeDataType("ABC")

        adaptProvider = customDataTypes.AdaptionProvider()
        with self.assertRaises(exceptions.NoValue):
            adaptProvider.convertDictToString({'col1': {}})

    def test_J_convertTupleToClsInstance(self):
        adaptProvider = customDataTypes.AdaptionProvider()
        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)

        adaptProvider.addDataType(dataType)

        testTuple = ('CUSTOM;MYCLS;VGVzdA==', 123, "CUSTOM;STR_ENCODED;Q1VTVE9NO2JsYWJsYWJsYQ==")

        converted = adaptProvider.convertTupleToClsInstance(testTuple)

        self.assertTrue(isinstance(converted[0], TestcustomDataTypes.MyClass))
        self.assertEqual(converted[0].arg, 'Test')

        self.assertEqual(converted[1], 123)
        self.assertEqual(converted[2], 'CUSTOM;blablabla')

    def test_K_convertDictToString(self):
        adaptProvider = customDataTypes.AdaptionProvider()

        testDict = {'col1': 123, 'col2': 'abc', 'col3': 'CUSTOM;anythinggoeshere'}

        converted = adaptProvider.convertDictToString(testDict)

        expected = {'col1': 123, 'col2': 'abc', 'col3': 'CUSTOM;STR_ENCODED;Q1VTVE9NO2FueXRoaW5nZ29lc2hlcmU='}

        self.assertEqual(converted, expected)

    def test_L_convertDictToString_customDataType(self):
        adaptProvider = customDataTypes.AdaptionProvider()
        dataType = customDataTypes.CustomDataType("MYCLS", TestcustomDataTypes.MyClass, TestcustomDataTypes.myClassToString, TestcustomDataTypes.stringToMyClass)

        adaptProvider.addDataType(dataType)

        clsInstance = TestcustomDataTypes.MyClass('Test')
        testDict = {'col1': {'value': clsInstance}, 'col2': {'value': 123, 'comparison': conditionEnums.ComparisonTypes.EQUAL_TO}}

        converted = adaptProvider.convertDictToString(testDict)

        expected =  {'col1': {'value': 'CUSTOM;MYCLS;VGVzdA=='}, 'col2': {'value': 123, 'comparison': conditionEnums.ComparisonTypes.EQUAL_TO}}

        self.assertEqual(converted, expected)

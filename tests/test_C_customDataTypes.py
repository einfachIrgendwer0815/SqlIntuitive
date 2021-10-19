from sqlIntuitive.ext import customDataTypes

import unittest

import json, os

defaultFile = 'tests/testsToRun.json'
altFile = 'tests/testsToRunDefault.json'

with open((defaultFile if os.path.exists(defaultFile) else altFile), 'r') as file:
    runTestCustomDataTypes = json.load(file)['customDataTypes']

@unittest.skipIf(runTestCustomDataTypes == False, 'Skipped TestDBSystems via config')
class TestcustomDataTypes(unittest.TestCase):
    def test_A_customDataType_init(self):
        class Test():
            pass

        def clsToString(clsInstance):
            return str(clsInstance)

        def stringToCls(string):
            return Test()

        customType = customDataTypes.CustomDataType("Test", Test, clsToString, stringToCls)

        self.assertEqual(customType.name, "TEST")

    def test_B_customDataType_convertToString(self):
        class TestB():
            def __init__(self, num):
                self.num = num

        def testBToString(instance):
            return str(instance.num)

        def stringToTestB(string):
            return TestB(int(string))

        customType = customDataTypes.CustomDataType("Test", TestB, testBToString, stringToTestB)

        self.assertEqual(customType.convertToString( TestB(123) ), "CUSTOM;TEST;MTIz")

        instance = customType.convertToClsInstance("CUSTOM;TEST;MTIz")
        self.assertTrue(isinstance(instance, TestB))
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
        class MyClass():
            def __init__(self, arg):
                self.arg = arg

        def myClassToString(clsInstance):
            return str(clsInstance.arg)

        def stringToMyClass(string):
            return MyClass(string)

        adaptProvider = customDataTypes.AdaptionProvider()

        dataType = customDataTypes.CustomDataType("MYCLS", MyClass, myClassToString, stringToMyClass)
        adaptProvider.addDataType(dataType)

        self.assertEqual(adaptProvider.convertToString(MyClass("abc")), "CUSTOM;MYCLS;YWJj")
        
        clsInstance = adaptProvider.convertToClsInstance("CUSTOM;MYCLS;YWJj")
        self.assertEqual(type(clsInstance), MyClass)
        self.assertEqual(clsInstance.arg, "abc")

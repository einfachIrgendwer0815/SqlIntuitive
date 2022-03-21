from base64 import b64encode, b64decode
from sqlIntuitive import exceptions

class CustomDataType():
    def __init__(self, name: str, cls, clsToStringFunc, stringToClsFunc):
        if type(name) != str:
            raise exceptions.NotAString(name)
        self.name = name.upper()

        if isinstance(cls, type) != True:
            raise exceptions.NotAClass(cls)
        self.cls = cls

        if hasattr(clsToStringFunc, '__call__') != True:
            raise exceptions.NotAFunction(clsToStringFunc)
        self.clsToStringFunc = clsToStringFunc

        if hasattr(stringToClsFunc, '__call__') != True:
            raise exceptions.NotAFunction(stringToClsFunc)
        self.stringToClsFunc = stringToClsFunc

    def convertToString(self, clsInstance) -> str:
        if type(clsInstance) != self.cls:
            raise exceptions.NotAMatchingClass(type(clsInstance), self.cls)

        convertedText = self.clsToStringFunc(clsInstance)

        if type(convertedText) != str:
            raise exceptions.NotAString(f"Return type of {self.clsToStringFunc}")

        convertedText = b64encode(convertedText.encode()).decode()

        fullText = f"CUSTOM;{self.name};{convertedText}"

        return fullText

    def convertToClsInstance(self, string: str):
        if type(string) != str:
            raise exceptions.NotAString(string)

        splitted = string.split(';')

        if splitted[1] != self.name:
            return string

        decodedText = b64decode(splitted[2]).decode()

        clsInstance = self.stringToClsFunc(decodedText)
        if isinstance(clsInstance, self.cls) != True:
            raise exceptions.NotAMatchingClass(type(clsInstance), self.cls)

        return clsInstance

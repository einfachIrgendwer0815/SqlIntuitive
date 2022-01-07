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

class AdaptionProvider():
    def __init__(self):
        self.types = {}
        self.clss = {}

        stringType = StringBypassType("STR_ENCODED")
        self.types[stringType.name] = stringType
        self.clss[stringType.cls] = stringType.name

    def addDataType(self, dataType: CustomDataType) -> None:
        if isinstance(dataType, CustomDataType):
            if dataType.name in self.types.keys() or dataType.cls in self.clss.keys():
                raise exceptions.DuplicationError(dataType.name, dataType.cls)

            self.types[dataType.name] = dataType
            self.clss[dataType.cls] = dataType.name

    def addDataType_raw(self, name: str, cls, clsToStringFunc, stringToClsFunc) -> None:
        dataType = CustomDataType(name, cls, clsToStringFunc, stringToClsFunc)

        self.addDataType(dataType)

    def removeDataType(self, name: str) -> None:
        if type(name) != str:
            raise exceptions.NotAString(name)

        if name.upper() == "STR_ENCODED":
            raise exceptions.DeletingTypeNotAllowed("It is not allowed to remove STR_ENCODED.")

        elif name.upper() not in self.types.keys():
            raise KeyError(f"{name}-type is not set.")

        cls = self.types[name].cls

        del self.clss[cls]
        del self.types[name]

    def convertToString(self, instance):
        if type(instance) in self.clss.keys():
            return self.types[self.clss[type(instance)]].convertToString(instance)
        else:
            return instance

    def convertToClsInstance(self, string: str) -> str:
        if type(string) != str:
            return string

        if string.startswith("CUSTOM;") != True:
            return string

        splitted = string.split(';')

        if splitted[1] not in self.types.keys():
            raise KeyError(f'Type {splitted[1]} is not registered')

        return self.types[splitted[1]].convertToClsInstance(string)

    def convertDictToString(self, dictionary: dict) -> dict:
        if type(dictionary) != dict:
            return dictionary

        dictionary = dictionary.copy()
        for key in dictionary.keys():
            if type(dictionary[key]) == dict:
                if 'value' not in dictionary[key].keys():
                    raise exceptions.NoValue(key)
                dictionary[key]['value'] = self.convertToString(dictionary[key]['value'])
            else:
                dictionary[key] = self.convertToString(dictionary[key])

        return dictionary

    def convertTupleToClsInstance(self, tupleToConvert: tuple) -> tuple:
        if type(tupleToConvert) != tuple:
            return tupleToConvert

        converted = []

        for item in tupleToConvert:
            converted.append(self.convertToClsInstance(item))

        return tuple(converted)

class StringBypassType(CustomDataType):
    def __init__(self, name: str):
        self.name = name
        self.cls = str

    def convertToString(self, clsInstance):
        if clsInstance.startswith("CUSTOM;"):
            encodedText = b64encode(clsInstance.encode()).decode()

            fullText = f"CUSTOM;{self.name};{encodedText}"

            return fullText
        else:
            return clsInstance

    def convertToClsInstance(self, string: str):
        splitted = string.split(';')

        decodedText = b64decode(splitted[2]).decode()

        return decodedText

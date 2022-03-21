from sqlIntuitive import exceptions
from sqlIntuitive.ext.customDataTypes.customType import CustomDataType
from sqlIntuitive.ext.customDataTypes.defaults import StringBypassType

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

from base64 import b64encode, b64decode

class AdaptionProvider():
    def __init__(self):
        self.types = {}
        self.clss = {}

        stringType = StringBypassType("STR_ENCODED")
        self.types[stringType.name] = stringType
        self.clss[stringType.cls] = stringType.name

        print(self.types['STR_ENCODED'])

    def addDataType(self, dataType):
        if isinstance(dataType, CustomDataType):
            if dataType.name in self.types.keys() or dataType.cls in self.clss.keys():
                raise exceptions.DuplicationError(f"{dataType.name} ({dataType.cls}) are already registered.")

            self.types[dataType.name] = dataType
            self.clss[dataType.cls] = dataType.name

    def convertToString(self, instance):
        if type(instance) in self.clss.keys():
            return self.types[self.clss[type(instance)]].convertToString(instance)
        else:
            return instance

    def convertToClsInstance(self, string):
        if type(string) != str:
            return string

        if string.startswith("CUSTOM;") != True:
            return string

        splitted = string.split(';')

        return self.types[splitted[1]].convertToClsInstance(string)

class CustomDataType():
    def __init__(self, name, cls, clsToStringFunc, stringToClsFunc):
        if type(name) != str:
            raise exceptions.NotAString(f"{type(name)} is not a string.")
        self.name = name.upper()

        if isinstance(cls, type) != True:
            raise exceptions.NotAClass(f"{cls} is not a class.")
        self.cls = cls

        if hasattr(clsToStringFunc, '__call__') != True:
            raise exceptions.NotAFunction(f"{clsToStringFunc} is not a function.")
        self.clsToStringFunc = clsToStringFunc

        if hasattr(stringToClsFunc, '__call__') != True:
            raise exceptions.NotAFunction(f"{stringToClsFunc} is not a function.")
        self.stringToClsFunc = stringToClsFunc

    def convertToString(self, clsInstance):
        if type(clsInstance) != self.cls:
            raise exceptions.NotAMatchingClass(f"{type(clsInstance)} does not match {self.cls}.")

        convertedText = self.clsToStringFunc(clsInstance)

        if type(convertedText) != str:
            raise exceptions.NotAString(f"{self.clsToStringFunc} did not return a string.")

        convertedText = b64encode(convertedText.encode()).decode()

        fullText = f"CUSTOM;{self.name};{convertedText}"

        return fullText

    def convertToClsInstance(self, string):
        if type(string) != str:
            raise exceptions.NotAString(f"{type(string)} is not a string.")

        splitted = string.split(';')

        if splitted[1] != self.name:
            return string

        decodedText = b64decode(splitted[2]).decode()

        clsInstance = self.stringToClsFunc(decodedText)
        if isinstance(clsInstance, self.cls) != True:
            raise exceptions.NotAMatchingClass(f"{type(clsInstance)} does not macht {self.cls}.")

        return clsInstance

class StringBypassType(CustomDataType):
    def __init__(self, name):
        self.name = name
        self.cls = str

    def convertToString(self, clsInstance):
        if clsInstance.startswith("CUSTOM;"):
            encodedText = b64encode(clsInstance.encode()).decode()

            fullText = f"CUSTOM;{self.name};{encodedText}"

            return fullText
        else:
            return clsInstance

    def convertToClsInstance(self, string):
        splitted = string.split(';')

        decodedText = b64decode(splitted[2]).decode()

        return decodedText
from base64 import b64encode, b64decode
from sqlIntuitive.ext.customDataTypes.customType import CustomDataType

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
#
#def listToStr(listObj: list) -> str:
#    pass
#
#def dictToStr(dictObj: dict) -> str:
#    pass
#
#def tupleToStr(tupleObj: tuple) -> str:
#    pass

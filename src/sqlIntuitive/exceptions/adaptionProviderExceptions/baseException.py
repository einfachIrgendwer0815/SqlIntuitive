from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class AdaptionProviderException(SqlIntuitiveException):
    def __str__(self):
        return "An overall exception was raised inside the class 'sqlIntuitive.ext.customDataTypes.AdaptionProvider'."

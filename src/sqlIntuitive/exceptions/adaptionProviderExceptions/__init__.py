from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class AdaptionProviderException(SqlIntuitiveException):
    pass

# AdaptionProviderExceptions

class DuplicationError(AdaptionProviderException):
    pass

class DeletingTypeNotAllowed(AdaptionProviderException):
    pass

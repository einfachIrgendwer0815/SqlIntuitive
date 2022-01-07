from sqlIntuitive.exceptions.parameterExceptions.baseException import ParameterException

class InvalidType(ParameterException):
    pass

class DictionaryEmptyException(ParameterException):
    pass

class InvalidTableNameException(ParameterException):
    pass

class InvalidDatabaseNameException(ParameterException):
    pass

class NotAClass(ParameterException):
    pass

class NotAFunction(ParameterException):
    pass

class NotAString(ParameterException):
    pass

class NotAMatchingClass(ParameterException):
    pass

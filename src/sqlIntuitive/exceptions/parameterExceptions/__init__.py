from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class ParameterException(SqlIntuitiveException):
    pass

# ParameterExceptions
class InvalidType(ParameterException):
    pass

class DictionaryEmptyException(ParameterException):
    pass

class InvalidTableNameException(ParameterException):
    pass

class InvalidDatabaseNameException(ParameterException):
    pass

class InvalidConstraint(ParameterException):
    pass

class NotAClass(ParameterException):
    pass

class NotAFunction(ParameterException):
    pass

class NotAString(ParameterException):
    pass

class NotAMatchingClass(ParameterException):
    pass

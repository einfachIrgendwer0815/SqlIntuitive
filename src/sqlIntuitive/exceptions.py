class SqlIntuitiveException(Exception):
    pass

class ParameterException(SqlIntuitiveException):
    pass

class DictionaryEmptyException(ParameterException):
    pass

class InvalidTableNameException(ParameterException):
    pass

class InvalidDatabaseNameException(ParameterException):
    pass

class InvalidConstrait(ParameterException):
    pass

class InvalidPrimaryKeyColumn(InvalidConstrait):
    pass

class InvalidForeignKeyColumn(InvalidConstrait):
    pass

class InvalidUniqueColumn(InvalidConstrait):
    pass

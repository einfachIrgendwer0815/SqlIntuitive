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

class InvalidConstraint(ParameterException):
    pass

class InvalidPrimaryKeyColumn(InvalidConstraint):
    pass

class InvalidForeignKeyColumn(InvalidConstraint):
    pass

class InvalidUniqueColumn(InvalidConstraint):
    pass

class InvalidNamedForeignKeyDictionary(InvalidConstraint):
    pass

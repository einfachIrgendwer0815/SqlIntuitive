from sqlIntuitive.exceptions.parameterExceptions import InvalidConstraint

class InvalidPrimaryKeyColumn(InvalidConstraint):
    pass

class InvalidForeignKeyColumn(InvalidConstraint):
    pass

class InvalidUniqueColumn(InvalidConstraint):
    pass

class InvalidNamedForeignKeyDictionary(InvalidConstraint):
    pass

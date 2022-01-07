from sqlIntuitive.exceptions.parameterExceptions.subexceptions.invalidConstraintExceptions.baseException import InvalidConstraint

class InvalidPrimaryKeyColumn(InvalidConstraint):
    def __init__(self, columnName):
        super().__init__()

        self.columnName = columnName

    def __str__(self):
        return f"{self.columnName} not in columns."

class InvalidForeignKeyColumn(InvalidConstraint):
    def __init__(self, columnName):
        super().__init__()

        self.columnName = columnName

    def __str__(self):
        return f"{self.columnName} not in columns."

class InvalidUniqueColumn(InvalidConstraint):
    def __init__(self, columnName):
        super().__init__()

        self.columnName = columnName

    def __str__(self):
        return f"{self.columnName} not in columns."

class InvalidNamedForeignKeyDictionary(InvalidConstraint):
    def __init__(self, columnName):
        super().__init__()

        self.columnName = columnName

    def __str__(self):
        return f"Values for column {self.columnName} are not defined."

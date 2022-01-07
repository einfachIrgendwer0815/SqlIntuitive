from sqlIntuitive.exceptions.parameterExceptions.baseException import ParameterException

class InvalidType(ParameterException):
    def __init__(self, value, expectedType):
        super().__init__()

        self.value = value
        self.expectedType = expectedType

    def __str__(self):
        return f"'{self.value}' is not an instance of {self.expectedType}."

class DictionaryEmptyException(ParameterException):
    def __init__(self, text):
        super().__init__()

        self.text = text

    def __str__(self):
        return self.text

class InvalidTableNameException(ParameterException):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Name for table contains invalid characters or is empty."

class InvalidDatabaseNameException(ParameterException):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Name for database contains invalid characters or is empty."

class NotAClass(ParameterException):
    def __init__(self, expectedAsCls):
        super().__init__()

        self.cls = expectedAsCls

    def __str__(self):
        return f"{self.cls} is not a class."

class NotAFunction(ParameterException):
    def __init__(self, expectedAsFunc):
        super().__init__()

        self.func = expectedAsFunc

    def __str__(self):
        return f"{self.func} is not a function."

class NotAString(ParameterException):
    def __init__(self, expectedAsString):
        super().__init__()

        self.string = expectedAsString

    def __str__(self):
        return f"{self.string} is not a string."

class NotAMatchingClass(ParameterException):
    def __init__(self, givenType, expectedType):
        super().__init__()

        self.givenType = givenType
        self.expectedType = expectedType

    def __str__(self):
        return f"{self.givenType} does not match {self.expectedType}."

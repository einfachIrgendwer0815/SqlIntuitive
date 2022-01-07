from sqlIntuitive.exceptions.conditionExceptions.baseException import ConditionException

class NotAComparisonType(ConditionException):
    def __init__(self, givenType):
        super().__init__()

        self.type = givenType

    def __str__(self):
        return f"{self.type} is not a comparison type."

class NotACombinationType(ConditionException):
    def __init__(self, givenType):
        super().__init__()

        self.type = givenType

    def __str__(self):
        return f"{self.type} is not a combination type."

class NoValue(ConditionException):
    def __init__(self, key):
        super().__init__()

        self.key = key

    def __str__(self):
        return f"No value for {self.key}."

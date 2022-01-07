from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class ConditionException(SqlIntuitiveException):
    pass

# ConditionExceptions

class NotAComparisonType(ConditionException):
    pass

class NotACombinationType(ConditionException):
    pass

class NoValue(ConditionException):
    pass

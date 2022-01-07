from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class ConditionException(SqlIntuitiveException):
    def __str__(self):
        return 'An overall \'Condition exception\' was raised processing a condition.'

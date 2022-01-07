from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class ParameterException(SqlIntuitiveException):
    def __str__(self):
        return "An overall \'Parameter exception\' was raised."

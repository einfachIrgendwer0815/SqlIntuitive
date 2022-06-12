from sqlIntuitive.exceptions import SqlIntuitiveException

class ProcedureException(SqlIntuitiveException):
    def __str__(self):
        return "An overall 'ProcedureException' was raised."

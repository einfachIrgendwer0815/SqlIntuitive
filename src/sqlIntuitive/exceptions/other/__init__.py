from sqlIntuitive.exceptions.baseException import SqlIntuitiveException

class NotSupported(SqlIntuitiveException):
    def __init__(self, featureName, dbSystemName):
        super().__init__()

        self.featureName = featureName
        self.dbSystemName = dbSystemName

    def __str__(self):
        return f"{self.featureName} is not supported in {self.dbSystemName}."

class CursorIsNone(SqlIntuitiveException):
    def __str__(self):
        return "Cursor was never created."

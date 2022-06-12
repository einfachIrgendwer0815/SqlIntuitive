from sqlIntuitive.exceptions.procedureExceptions.baseException import ProcedureException

class InvalidCommand(ProcedureException):
    def __init__(self, command):
        super().__init__()

        self.command = command

    def __str__(self):
        return f"Command '{self.command}' is invalid."

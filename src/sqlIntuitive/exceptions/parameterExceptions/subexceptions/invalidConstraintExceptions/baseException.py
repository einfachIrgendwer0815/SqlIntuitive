from sqlIntuitive.exceptions.parameterExceptions.baseException import ParameterException

class InvalidConstraint(ParameterException):
    def __str__(self):
        return "An overall \'Invalid constraint\' parameter exception was raised."

from sqlIntuitive.exceptions.adaptionProviderExceptions.baseException import AdaptionProviderException

class DuplicationError(AdaptionProviderException):
    def __init__(self, name, cls):
        super().__init__()

        self.name = name
        self.cls = cls

    def __str__(self):
        return f"{self.name} ({self.cls}) are already registered."


class DeletingTypeNotAllowed(AdaptionProviderException):
    def __init__(self, name):
        super().__init__()

        self.name = name

    def __str__(self):
        return f"It is not allowed to remove {self.name}."

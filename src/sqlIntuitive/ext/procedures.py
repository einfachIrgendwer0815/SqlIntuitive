class Procedure():
    def __init__(self, commands: list = None):
        self._featuresUsed = 0

        self.commands = []

    def _check_command_list_validity(self, command_list: list):
        pass

    def getFeaturesUsed(self):
        return self._featuresUsed

    def __len__(self):
        return len(self.commands)

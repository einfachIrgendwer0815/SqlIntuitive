from sqlIntuitive.sqlGeneration import functionEnums
from sqlIntuitive.exceptions import InvalidCommand
from typing import types

class Procedure():
    COMMAND_STRUCTURE = {
        "operation": types.FunctionType,
        "args": list,
        "kwargs": dict,
    }

    def __init__(self, commands: list = []):
        self._featuresUsed = 0

        self.commands = []

        for command in commands:
            if self._check_command_validity(command):
                self.commands.append(command)
            else:
                raise InvalidCommand(command)

    def _check_command_validity(self, command):
        for key, value_type in Procedure.COMMAND_STRUCTURE.items():
            if key not in command.keys() or type(command[key]) != value_type:
                return False

        return True

    def __len__(self):
        return len(self.commands)

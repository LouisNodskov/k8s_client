from .abstract_base_command import Command

class Invoker(object):
    def __init__(self):
        self.commands : list[Command] = []

    def add_command(self, command : Command) -> 'Invoker':
        self.commands.append(command)
        return self

    def run(self) -> 'Invoker':
        for command in self.commands:
            command.execute()
        self.__clear_commands()
        return self

    def __clear_commands(self):
        self.commands = []
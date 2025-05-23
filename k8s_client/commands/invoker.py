from k8s_client.commands.abstract_command_base import Command

class Invoker(object):
    def __init__(self):
        self.commands : list[Command] = []

    def add_command(self, command : Command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command.execute()
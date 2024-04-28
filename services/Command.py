class Command:
    def __init__(self, command: str, **parameters):
        self.command = command
        self.parameters = parameters

    def getParameter(self, name: str):
        return self.parameters.get(name)

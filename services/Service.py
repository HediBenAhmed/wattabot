from multiprocessing import Process, Queue
from services.Command import Command


class Service:
    def __init__(self, name: str):
        self.queue = Queue()
        self.name = name

    def consume(self):
        while True:
            command = self.queue.get()
            if command is None:
                break
            self.executeCommand(command)

    def executeCommand(self, command: Command):
        pass

    def sendCommand(self, service, command: Command):
        queue: Queue = service.queue
        queue.put(command)

    def getStatus(self):
        pass

    def startConsumer(self):
        service = Process(target=self.consume, args=())
        service.start()

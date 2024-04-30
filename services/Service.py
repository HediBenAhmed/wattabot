from multiprocessing import Process, Queue, Manager
import threading
from typing import List
from services.Command import Command

SHARED_DICT = Manager().dict()


class Service:
    def __init__(self, name: str):
        self.queue = Queue()
        self.name = name

    def consumeQueue(self):
        while True:
            command = self.queue.get()
            if command is None:
                break
            self.executeCommand(command)

    def executeCommand(self, command: Command):
        pass

    def executeSubTasks(self, functions: List[tuple]):

        threads = []
        for function in functions:
            threads.append(threading.Thread(target=function[0], args=function[1]))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def sendCommand(self, service, command: Command):
        queue: Queue = service.queue
        queue.put(command)

    def save(self, key: str, value):
        SHARED_DICT[key] = value

    def get(self, key: str):
        if key in SHARED_DICT:
            return SHARED_DICT[key]

        return None

    def startConsumer(self, consumer):
        service = Process(target=consumer, args=())
        service.start()

    def startProducer(self, producer):
        service = Process(target=producer, args=())
        service.start()

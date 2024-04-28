import asyncio
from concurrent.futures import ProcessPoolExecutor
import threading
from typing import List
from services.Command import Command

processPoolExecutor = ProcessPoolExecutor(max_workers=4)
eventLoop = asyncio.get_event_loop()


class Service:
    def executeCommand(self, command: Command):
        pass

    def sendCommand(self, service, command: Command):

        return eventLoop.run_until_complete(
            asyncio.gather(
                eventLoop.run_in_executor(
                    processPoolExecutor, service.executeCommand, command
                )
            )
        )

    def executeTasks(self, functions: List[tuple]):

        threads = []
        for function in functions:
            threads.append(threading.Thread(target=function[0], args=function[1]))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

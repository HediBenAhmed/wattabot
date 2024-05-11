import threading
from typing import List


class Service:
    def executeSubTasks(self, functions: List[tuple]):

        threads = []
        for function in functions:
            threads.append(threading.Thread(target=function[0], args=function[1]))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

from multiprocessing import Manager


class ProcessManager:
    def __init__(self):
        self.manager = Manager()
        self.processStatus = self.manager.dict()

    def updateProcessStatus(self, name: str, status):
        self.processStatus[name] = vars(status)

    def getProcessStatus(self, name: str, key: str):
        return self.processStatus[name][key]


PROCESS_MANAGER = ProcessManager()


class Status:
    pass

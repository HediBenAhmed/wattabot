from multiprocessing import Lock


class Device:
    def __init__(self):
        self.lock = Lock()

    def lockDevice(self):
        self.lock.acquire()

    def releaseDevice(self):
        self.lock.release()

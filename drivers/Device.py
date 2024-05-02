from multiprocessing import Lock
import threading


class Device:
    def __init__(self):
        self.lock = threading.Lock()

    def lockDevice(self):
        self.lock.acquire()

    def releaseDevice(self):
        self.lock.release()

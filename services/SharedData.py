from multiprocessing import Manager
from time import sleep

SHARED_DICT = Manager().dict()


def setSharedData(key: str, value):
    SHARED_DICT[key] = value


def getSharedData(key: str, maxRetry=20, retry=0):
    if key in SHARED_DICT:
        return SHARED_DICT[key]

    elif retry < maxRetry:
        sleep(0.1)
        print(key, "no value, retry", retry + 1)
        return getSharedData(key, maxRetry, retry + 1)

    return None

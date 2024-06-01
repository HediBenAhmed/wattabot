from multiprocessing import Process
from threading import Thread
from time import sleep
from typing import List

SHARED_DICT = dict()


def startJobInLoop(job, jobName: str):
    if getSharedData(key=jobName, maxRetry=0):
        print(jobName, "already running")
        return None, None

    setSharedData(jobName, True)

    def jobLoop():
        while getSharedData(key=jobName, maxRetry=0):
            job()

        print("END JOB", jobName)

    print("START JOB", jobName)
    service = Thread(target=jobLoop, args=(), name=jobName)
    service.start()
    return service, jobName


def stopJobInLoop(jobName: str):
    setSharedData(jobName, False)


def startProcess(job, jobName: str):
    if getSharedData(key=jobName, maxRetry=0):
        print(jobName, "already running")
        return None, None

    setSharedData(jobName, True)

    print("START FEATURE", jobName)
    service = Process(target=job, args=(), name=jobName)
    service.start()
    return service, jobName


def stopProcess(job: Process, jobName: str):
    print("END FEATURE", jobName)
    job.kill()
    setSharedData(jobName, False)


def executeTasks(functions: List[tuple]):

    threads = []
    for function in functions:
        threads.append(Thread(target=function[0], args=function[1]))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def setSharedData(key: str, value):
    SHARED_DICT[key] = value


def getSharedData(key: str, maxRetry=20, retryDelay=0.2, retry=0):
    if key in SHARED_DICT:
        return SHARED_DICT[key]

    elif retry < maxRetry:
        sleep(retryDelay)
        print(key, "no value, retry", retry + 1)
        return getSharedData(key, maxRetry, retryDelay, retry + 1)

    return None

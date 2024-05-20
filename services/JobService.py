from multiprocessing import Process
from threading import Thread
from time import sleep
from typing import List


def startJobInLoop(job, jobName: str, sharedDict, delay: float = 0):
    if getSharedData(key=jobName, sharedDict=sharedDict, maxRetry=0):
        print(jobName, "already running")
        return None, None

    setSharedData(jobName, True, sharedDict)

    def jobLoop():
        while getSharedData(key=jobName, maxRetry=0, sharedDict=sharedDict):
            job()
            sleep(delay)

        print("END JOB", jobName)

    print("START JOB", jobName)
    service = Thread(target=jobLoop, args=(), name=jobName)
    service.start()
    return service, jobName


def stopJobInLoop(jobName: str, sharedDict):
    setSharedData(jobName, False, sharedDict)


def startProcess(job, jobName: str, sharedDict):
    if getSharedData(key=jobName, sharedDict=sharedDict, maxRetry=0):
        print(jobName, "already running")
        return None, None

    setSharedData(jobName, True, sharedDict)

    print("START FEATURE", jobName)
    service = Process(target=job, args=(), name=jobName)
    service.start()
    return service, jobName


def stopProcess(job: Process, jobName: str, sharedDict):
    print("END FEATURE", jobName)
    job.kill()
    setSharedData(jobName, False, sharedDict)


def executeTasks(functions: List[tuple]):

    threads = []
    for function in functions:
        threads.append(Thread(target=function[0], args=function[1]))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def setSharedData(key: str, value, sharedDict):
    sharedDict[key] = value


def getSharedData(key: str, sharedDict, maxRetry=20, retry=0):
    if key in sharedDict:
        return sharedDict[key]

    elif retry < maxRetry:
        sleep(0.1)
        print(key, "no value, retry", retry + 1)
        return getSharedData(key, sharedDict, maxRetry, retry + 1)

    return None

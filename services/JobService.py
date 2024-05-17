from threading import Thread
from time import sleep
from typing import List
from services.SharedData import getSharedData, setSharedData


def startJobInLoop(job, jobName: str, delay: float = 0):
    if getSharedData(key=jobName, maxRetry=0):
        print(jobName, "already running")
        return

    setSharedData(jobName, True)

    def jobLoop():
        while getSharedData(key=jobName, maxRetry=0):
            job()
            sleep(delay)

        print("END JOB", jobName)

    print("START JOB", jobName)
    service = Thread(target=jobLoop, args=(), name=jobName)
    service.start()
    return service, jobName


def stopJobInLoop(jobName: str):
    setSharedData(jobName, False)


def startJob(job, jobName: str):
    if getSharedData(key=jobName, maxRetry=0):
        print(jobName, "already running")
        return

    setSharedData(jobName, True)

    print("START JOB", jobName)
    service = Thread(target=job, args=(), name=jobName)
    service.start()
    return service, jobName


def executeTasks(functions: List[tuple]):

    threads = []
    for function in functions:
        threads.append(Thread(target=function[0], args=function[1]))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

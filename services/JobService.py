from threading import Thread
from time import sleep
from services.SharedData import getSharedData, saveSharedData


def startJobInLoop(job, jobName: str, delay: float = 0):
    if getSharedData(key=jobName, maxRetry=0):
        print(jobName, "already running")
        return

    saveSharedData(jobName, True)

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
    saveSharedData(jobName, False)

from time import sleep
from feature.Feature import Feature
from services.JobService import startJobInLoop, startProcess, stopJobInLoop, stopProcess
from services.OLEDService import OLEDService


class SystemInfo(Feature):

    def start(self):

        def job():
            OLEDService.getInsance().displaySystemInfo()
            sleep(3)

        thread, threadName = startJobInLoop(job=job, jobName="displaySystemInfo")

        if threadName is not None:
            self.threadName = threadName

    def stop(self):
        stopJobInLoop(self.threadName)

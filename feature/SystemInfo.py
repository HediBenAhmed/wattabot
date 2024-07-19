from time import sleep
from feature.Feature import Feature
from services.JobService import startJobInLoop, stopJobInLoop
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
        if self.threadName is not None:
            stopJobInLoop(self.threadName)
            OLEDService.getInsance().clear()

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif action == "STOP":
            self.stop()

        return "systemInfo {}".format(action)

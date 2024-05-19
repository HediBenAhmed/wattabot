from time import sleep
from feature.Feature import Feature
from services.JobService import startProcess, stopProcess
from services.OLEDService import OLEDService


class SystemInfo(Feature):

    def start(self, sharedDict):

        def job():
            oledService = OLEDService.getInsance()
            while True:
                oledService.displaySystemInfo()
                sleep(2)

        process, _ = startProcess(
            job,
            "displaySystemInfo",
            sharedDict,
        )
        self.process = process

    def stop(self, sharedDict):
        stopProcess(self.process, "displaySystemInfo", sharedDict)

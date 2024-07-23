from time import sleep
from drivers.Camera import CAMERA_FPS
from feature.Feature import Feature
from services.CameraServoService import CameraServoService
from services.BodyIdentifierService import BodyIdentifierService

from services.JobService import (
    getSharedData,
    startJobInLoop,
    stopJobInLoop,
)


class FolowObject(Feature):

    def start(self):

        def job():
            sleep(1 / CAMERA_FPS)
            frame = getSharedData("camera.frame")
            keypoints = BodyIdentifierService.getInsance().reconizeBody_tf(frame)

            # for i in range(17):
            #     frame = cv2.circle(
            #         frame,
            #         (int(keypoints[i][0]), int(keypoints[i][1])),
            #         radius=5,
            #         color=(0, 0, 255),
            #         thickness=-1,
            #     )

            # frame = setSharedData("camera.frame", frame)

            nosePoint = BodyIdentifierService.getInsance().getNosePoint(keypoints)
            if nosePoint is not None:
                CameraServoService.getInsance().centralizeFace2(nosePoint)

        thread, threadName = startJobInLoop(job=job, jobName="folowObject")

        if threadName is not None:
            self.threadName = threadName

    def stop(self):
        if self.threadName is not None:
            stopJobInLoop(self.threadName)

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif action == "STOP":
            self.stop()

        return "folowObject {}".format(action)

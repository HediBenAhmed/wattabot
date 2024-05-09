from drivers.Device import Device
import cv2
from services.Configurations import cameraConfig
from services.JobService import startJobInLoop
from services.SharedData import setSharedData
import numpy as np

CAMERA_FPS = cameraConfig("FPS")
CAMERA_WIDTH = cameraConfig("WIDTH")
CAMERA_HEIGHT = cameraConfig("HEIGHT")


class Camera(Device):
    def __init__(self, width=1280, height=720):
        super().__init__()
        self.cap = cv2.VideoCapture(cameraConfig("INDEX"))
        self.setCameraConfigs(width, height)

    def adjustGamma(self, frame, gamma=1.0):
        if gamma == 1.0:
            return frame

        invGamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")

        return cv2.LUT(frame, table)

    def getImage(self, gamma=1.0):
        ref, frame = self.cap.read()

        return ref, self.adjustGamma(frame, gamma)

    def setCameraConfigs(self, width: int, height: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def setDefaultCameraConfigs(self):
        self.setCameraConfigs(CAMERA_WIDTH, CAMERA_HEIGHT)

    def streamImages(self, output: str):
        def job():
            ref, frame = self.getImage()
            setSharedData(output, frame)

        return startJobInLoop(job=job, jobName="streamImages", delay=1 / CAMERA_FPS)

    def getWidth(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def getHeight(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

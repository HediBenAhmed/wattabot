from typing import List
from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH, Camera
import cv2
from services.Face import Face
from services.Service import Service

NAMES = [
    "",
    "hedi",
]  # key in names, start from the second place, leave first empty

CENTER_OF_CAMERA = [CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2]
CENTER_MARGIN = [50, 50]


class CameraService(Service):

    def __init__(self):
        self.CAMERA = Camera(CAMERA_WIDTH, CAMERA_HEIGHT)

    def getImage(self, gamma=1.0):
        ret, frame = self.CAMERA.getImage(gamma)
        return ret, frame

    def saveImage(self, frame, output):
        cv2.imwrite(output, frame)

    def setMaxResolution(self):
        self.CAMERA.setCameraConfigs(1280, 720)

    def setDefaultCameraConfigs(self):
        self.CAMERA.setDefaultCameraConfigs()

    @classmethod
    def createInstance(self):
        return CameraService()

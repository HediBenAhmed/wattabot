from drivers.Device import Device
import cv2
from services.Configurations import cameraConfig

CAMERA_FPS = cameraConfig("FPS")
CAMERA_WIDTH = cameraConfig("WIDTH")
CAMERA_HEIGHT = cameraConfig("HEIGHT")


class Camera(Device):
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(cameraConfig("INDEX"))
        self.setCameraConfigs(width, height)

    def getImage(self):
        return self.cap.read()

    def setCameraConfigs(self, width: int, heigth: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigth)
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


CAMERA = Camera(CAMERA_WIDTH, CAMERA_HEIGHT)

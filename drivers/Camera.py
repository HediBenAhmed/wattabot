from drivers.Device import Device
import cv2


class Camera(Device):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def read(self, output: str):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(output, frame)

    def setCameraResolution(self, width: int, heigth: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigth)

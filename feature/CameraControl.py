from feature.Feature import Feature
from services.CameraServoService import CameraServoService


class CameraControl(Feature):
    def start(self):
        self.service = CameraServoService.getInsance()

    def execute(self, action: str):
        hStep = 0
        vStep = 0
        if action == "CAM_N":
            hStep = 0
            vStep = -2
        elif action == "CAM_S":
            hStep = 0
            vStep = 2
        elif action == "CAM_W":
            hStep = 2
            vStep = 0
        elif action == "CAM_E":
            hStep = -2
            vStep = 0
        elif action == "CAM_NW":
            hStep = 2
            vStep = -2
        elif action == "CAM_NE":
            hStep = -2
            vStep = -2
        elif action == "CAM_SW":
            hStep = 2
            vStep = 2
        elif action == "CAM_SE":
            hStep = -2
            vStep = 2

        self.service.move(hStep, vStep)

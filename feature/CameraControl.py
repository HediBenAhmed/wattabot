from feature.Feature import Feature
from services.CameraServoService import CameraServoService


class CameraControl(Feature):
    def start(self):
        self.service = CameraServoService.getInsance()
        self.started = True

    def stop(self):
        self.started = False

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif not self.started:
            print("cameraControl disabled")
        elif action == "STOP":
            self.stop()
        elif action == "CAM_N":
            self.service.move(0, -2)
        elif action == "CAM_S":
            self.service.move(0, 2)
        elif action == "CAM_W":
            self.service.move(2, 0)
        elif action == "CAM_E":
            self.service.move(-2, 0)
        elif action == "CAM_NW":
            self.service.move(2, -2)
        elif action == "CAM_NE":
            self.service.move(-2, -2)
        elif action == "CAM_SW":
            self.service.move(2, 2)
        elif action == "CAM_SE":
            self.service.move(-2, 2)

        return "cameraControl {}".format(action)

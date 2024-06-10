from feature.Feature import Feature
from services.CameraServoService import CameraServoService
from services.MotorsService import MotorsService


class MotorsControl(Feature):
    def start(self):
        self.service = MotorsService.getInsance()
        self.started = True

    def stop(self):
        self.started = False

    def execute(self, action: str):
        if not self.started:
            print("motorsControl disabled")
        elif action == "START":
            self.start()
        elif action == "STOP":
            self.stop()
        elif action == "MOTOR_N":
            self.service.forward()
        elif action == "MOTOR_S":
            self.service.backward()
        elif action == "MOTOR_W":
            self.service.left()
        elif action == "MOTOR_E":
            self.service.right()
        elif action == "MOTOR_NW":
            self.service.left()
        elif action == "MOTOR_NE":
            self.service.right()
        elif action == "MOTOR_SW":
            self.service.left()
        elif action == "MOTOR_SE":
            self.service.right()
        elif action == "MOTOR_C":
            self.service.stop()

        return "motorsControl {}".format(action)

from services.SocketService import SocketService
import threading
from drivers.Servo import SERVO_CAMERA_H, SERVO_CAMERA_V

PORT = 1050


class CameraService(SocketService):
    def __init__(self):
        super().__init__(PORT)

    def runAction(self, action: str):
        h = action.split(",")[0]
        v = action.split(",")[1]

        t1 = threading.Thread(target=self.moveHorizontal, args=(h,))
        t2 = threading.Thread(target=self.moveVertical, args=(v,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def moveHorizontal(self, angle):
        SERVO_CAMERA_H.goToAngle(float(angle))

    def moveVertical(self, angle):
        SERVO_CAMERA_V.goToAngle(float(angle))

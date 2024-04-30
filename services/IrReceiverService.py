from drivers.IrReceiver import IR_RECEIVER, KEY_UP, KEY_DOWN, NONE
from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.Command import Command
from services.Service import Service


class IrReceiver(Service):

    def readKey(self):

        keyPressed = False
        while True:
            key = IR_RECEIVER.readKey()

            if key == KEY_UP:
                keyPressed = True
                self.sendCommand(
                    CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=-1)
                )
            if key == KEY_DOWN:
                self.sendCommand(
                    CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=1)
                )
            if key == NONE and keyPressed:
                print("END")
                keyPressed = False


IR_RECEIVER_SERVICE = IrReceiver("IR_RECEIVER_SERVICE")

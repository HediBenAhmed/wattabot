from drivers.IrReceiver import *
from services.Service import Service


class IrReceiverService(Service):

    def readKey(self):

        keyPressed = False
        while True:
            key = IR_RECEIVER.readKey()

            if key == NONE and keyPressed:
                print("END")
                keyPressed = False

    @classmethod
    def createInstance(self):
        return IrReceiverService()

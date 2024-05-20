from drivers.IrReceiver import NONE, IR_RECEIVER
from services.Service import Service


class IrReceiverService(Service):

    def readKey(self):
        key = NONE
        while key == NONE:
            key = IR_RECEIVER.readKey()

        return key

    @classmethod
    def createInstance(self):
        return IrReceiverService()

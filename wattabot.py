from multiprocessing import Manager
from feature.SystemInfo import SystemInfo
from services.IdentificationService import IdentificationService
from services.IrReceiverService import IrReceiverService
from services.User import User
from feature.WebControl import WebControl
from drivers.IrReceiver import KEY_0, KEY_1, KEY_2

FEATURES = {"systemInfo": SystemInfo(), "webControl": WebControl()}
SHARED_DICT = Manager().dict()

FEATURES_KEYS = {KEY_1: "webControl", KEY_2: "systemInfo"}

AUTO_FEATURES = {"systemInfo": True, "webControl": True}


def startModules(features):

    for feature, enabled in features.items():
        if enabled:
            FEATURES[feature].start(SHARED_DICT)


def startModule(key, features):
    if key in FEATURES_KEYS:
        feature = FEATURES_KEYS[key]
        enabled = features[feature]
        if enabled:
            FEATURES[feature].start(SHARED_DICT)


if __name__ == "__main__":

    user: User = IdentificationService.getInsance().identification()
    if user is not None:
        usrFeatures = user.userSettings["features"]
        command = None
        while command != KEY_0:
            command = IrReceiverService.getInsance().readKey()
            startModule(command, usrFeatures)

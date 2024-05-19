from multiprocessing import Manager
from feature.SystemInfo import SystemInfo
from services.IdentificationService import IdentificationService
from services.User import User
from feature.WebControl import WebControl


FEATURES = {"systemInfo": SystemInfo(), "webControl": WebControl()}
SHARED_DICT = Manager().dict()


def startModules(features):

    for feature, enabled in features.items():
        if enabled:
            FEATURES[feature].start(SHARED_DICT)


if __name__ == "__main__":

    user: User = IdentificationService.getInsance().identification()
    if user is not None:
        startModules(user.userSettings["features"])

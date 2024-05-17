from identification import identification
from services.JobService import startJob, startJobInLoop
from services.OLEDService import OLEDService
from services.User import User
from web import startServer


def webControl():
    return startJob(startServer, "webserver")


def systemInfo():
    return startJobInLoop(
        OLEDService.getInsance().displaySystemInfo, "displaySystemInfo", 2
    )


def startModules(features):
    if features["webControl"]:
        webControl()

    if features["systemInfo"]:
        systemInfo()


if __name__ == "__main__":
    user: User = identification()

    if user is not None:
        startModules(user.userSettings["features"])

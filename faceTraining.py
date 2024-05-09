import os
from time import sleep
from typing import List
from drivers.Camera import CAMERA_FPS
from services.CameraService import CAMERA_SERVICE
from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.Face import Face
from services.LEDService import LED_SERVICE
from drivers.LED import one, two, three, four, five, matrix_allow, matrix_deny
import fnmatch

path = "/home/hedi/wattabot/trainer"
name = "hedi"
gamma = 1


def countTrainImages(dataPath):
    count = len(fnmatch.filter(os.listdir(dataPath), "*.jpg"))
    return count


def waitForFace():
    CAMERA_SERVO_SERVICE.setPosition(0, -0.0)
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces_dnn(frame)
        if len(faces) > 0:
            return faces[0]
        sleep(2 / CAMERA_FPS)


def centralizeFace():
    while True:
        sleep(1 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces_dnn(frame)
        if len(faces) > 0:
            h, v = CAMERA_SERVO_SERVICE.centralizeFace(faces[0])

            if h == 0 and v == 0:
                return


def dataCollect():
    dataDirectory = os.path.join(path, "data", name)

    if not os.path.exists(dataDirectory):
        os.makedirs(dataDirectory)
        totalCount = 0
    else:
        totalCount = countTrainImages(dataDirectory)
    count = 1
    while True:
        print(count, "%")
        if count > 100:
            return

        sleep(1 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces_dnn(frame)

        if len(faces) != 1:
            print("no faces")
            continue

        CAMERA_SERVICE.saveImage(
            faces[0].image,
            dataDirectory + "/" + str(count + totalCount) + ".jpg",
        )

        count += 1


def trainingModel():
    CAMERA_SERVICE.trainModel_dnn(path)


def testModel():
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces_dnn(frame)
        if len(faces) > 0:
            faces = CAMERA_SERVICE.identifyFaces_dnn(faces)
            if faces[0].identified:
                print(faces[0].name, faces[0].confidence, faces[0].identified)
                return
        sleep(2 / CAMERA_FPS)


def fraceTraining():
    try:
        LED_SERVICE.clear()
        CAMERA_SERVICE.setDefaultCameraConfigs()

        LED_SERVICE.display(one)
        waitForFace()

        LED_SERVICE.display(two)
        centralizeFace()

        LED_SERVICE.display(three)
        dataCollect()

        LED_SERVICE.display(four)
        trainingModel()

        LED_SERVICE.display(five)
        testModel()

        LED_SERVICE.display(matrix_allow)
    except Exception as error:
        LED_SERVICE.display(matrix_deny)
        print("An exception occurred:", error)


if __name__ == "__main__":
    fraceTraining()

import os
from time import sleep
from typing import List
from drivers.Camera import CAMERA_FPS
from services.CameraService import CameraService
from services.CameraServoService import CameraServoService
from services.Face import Face
from services.FaceClassifierService import FaceClassfifierService
from services.LEDService import LEDService
from drivers.LED import one, two, three, four, five, matrix_allow, matrix_deny
import fnmatch

name = "hedi"
gamma = 1

CAMERA_SERVICE: CameraService = CameraService.getInsance()
CAMERA_SERVO_SERVICE: CameraServoService = CameraServoService.getInsance()
FACE_SERVICE: FaceClassfifierService = FaceClassfifierService.getInsance()


def countTrainImages(dataPath):
    count = len(fnmatch.filter(os.listdir(dataPath), "*.jpg"))
    return count


def waitForFace():
    CAMERA_SERVO_SERVICE.setPosition(0, -0.0)
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = FACE_SERVICE.idenfiyFaces(frame)
        if len(faces) > 0:
            return faces[0]
        sleep(2 / CAMERA_FPS)


def centralizeFace():
    while True:
        sleep(1 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = FACE_SERVICE.idenfiyFaces(frame)
        if len(faces) > 0:
            h, v = CAMERA_SERVO_SERVICE.centralizeFace(faces[0])

            if h == 0 and v == 0:
                return


def dataCollect():
    dataDirectory = os.path.join("/home/hedi/wattabot/trainer/data", name)

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
        faces: List[Face] = FACE_SERVICE.idenfiyFaces(frame)

        if len(faces) != 1:
            print("no faces")
            continue

        CAMERA_SERVICE.saveImage(
            faces[0].image,
            dataDirectory + "/" + str(count + totalCount) + ".jpg",
        )

        count += 1


def trainingModel():
    FACE_SERVICE.trainModel_dnn()


def testModel():
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = FACE_SERVICE.idenfiyFaces(frame)
        if len(faces) > 0:
            faces = FACE_SERVICE.reconizeFaces_dnn(faces)
            if faces[0].identified:
                print(faces[0].name, faces[0].confidence, faces[0].identified)
                return
        sleep(2 / CAMERA_FPS)


def fraceTraining():
    LED_SERVICE: LEDService = LEDService.getInsance()
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

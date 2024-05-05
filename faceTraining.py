import numpy as np
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
id = "1"
gamma = 1


def countTrainImages():
    dir_path = path + "/data"
    count = len(fnmatch.filter(os.listdir(dir_path), "User." + id + ".*.jpg"))
    return count


def waitForFace():
    CAMERA_SERVO_SERVICE.setPosition(0, -0.20)
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces(frame, False)
        if len(faces) > 0:
            return faces[0]
        sleep(2 / CAMERA_FPS)


def centralizeFace():
    while True:
        sleep(1 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces(frame, False)
        if len(faces) > 0:
            h, v = CAMERA_SERVO_SERVICE.centralizeFace(faces[0])

            if h == 0 and v == 0:
                return


def dataCollect():
    totalCount = countTrainImages()
    count = 1
    while True:
        print(count, "%")
        if count > 100:
            return

        sleep(1 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces(frame, False)

        if len(faces) != 1:
            print("no faces")
            continue

        CAMERA_SERVICE.saveImage(
            faces[0].image,
            path + "/data/User." + id + "." + str(count + totalCount) + ".jpg",
        )

        count += 1


def trainingModel():
    faces, ids = CAMERA_SERVICE.getImagesAndLabels(path)
    CAMERA_SERVICE.trainModel(path, faces, np.array(ids))


def testModel():
    while True:
        ret, frame = CAMERA_SERVICE.getImage(gamma)
        faces: List[Face] = CAMERA_SERVICE.scanFaces(frame)
        if len(faces) > 0:
            CAMERA_SERVO_SERVICE.centralizeFace(faces[0])
            print(faces[0].name, faces[0].confidence, faces[0].identified)
            if faces[0].identified:
                return
        sleep(2 / CAMERA_FPS)


if __name__ == "__main__":
    try:
        LED_SERVICE.clear()
        CAMERA_SERVICE.setDefaultCameraConfigs()

        LED_SERVICE.display(one)
        waitForFace()

        LED_SERVICE.display(two)
        centralizeFace()

        LED_SERVICE.display(three)
        CAMERA_SERVICE.setMaxResolution()
        dataCollect()

        LED_SERVICE.display(four)
        trainingModel()

        LED_SERVICE.display(five)
        testModel()

        LED_SERVICE.display(matrix_allow)
    except Exception as error:
        LED_SERVICE.display(matrix_deny)
        print("An exception occurred:", error)

import time
from typing import List

from drivers.Camera import CAMERA_FPS, CAMERA_HEIGHT, CAMERA_WIDTH, CAMERA
import cv2
import numpy as np

from services.Command import Command
from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.Face import Face
from services.Service import Service

FACE_DETECTOR = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
RECONIZER = cv2.face.LBPHFaceRecognizer_create()
RECONIZER.read("/home/hedi/wattabot/trainer/trainer.yml")  # load trained model

NAMES = [
    "",
    "hedi",
]  # key in names, start from the second place, leave first empty

CENTER_OF_CAMERA = [CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2]
CENTER_MARGIN = [50, 50]


class CameraService(Service):

    def getImage(self, gamma=1.0):
        ret, frame = CAMERA.getImage()
        if ret and gamma != 1.0:
            frame = self.adjustGamma(frame, gamma)
        return ret, frame

    def centralizeFace(self):
        pass

    def scanFaces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []
        f = FACE_DETECTOR.detectMultiScale(
            image=gray, scaleFactor=1.2, minNeighbors=2, minSize=(30, 30)
        )
        for x, y, w, h in f:
            id, confidence = RECONIZER.predict(gray[y : y + h, x : x + w])
            # Check if confidence is less then 40  ==> "0" is perfect match
            if confidence < 49:
                id = NAMES[id]
            else:
                id = "unknown"

                confidence = round(100 - confidence)
            faces.append(
                Face(
                    gray[x : x + w, y : y + h],
                    [x, y, w, h],
                    True,
                    id,
                    confidence,
                )
            )

        return faces

    def lookupForFaces(self):
        faces = []
        self.sendCommand(CAMERA_SERVO_SERVICE, Command("setPosition", x=0, y=0.45))

        foundFace = False
        centralized = False
        while not centralized and not (
            CAMERA_SERVO_SERVICE.getStatus().vservoMax
            or CAMERA_SERVO_SERVICE.getStatus().hservoMax
        ):
            if not foundFace:
                self.sendCommand(
                    CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=2)
                )
            time.sleep(2 / CAMERA_FPS)
            ret, frame = CAMERA.getImage()
            if ret:
                faces = self.scanFaces(frame, False)

                if len(faces) > 0:
                    foundFace = True
                    face = faces[0]
                    moveTo = self.centralizeFace(face)

                    if moveTo == [0, 0]:
                        centralized = True

        # identify face
        CAMERA.setCameraConfigs(width=1280, height=720)
        ret, frame = CAMERA.getImage()
        if ret:
            faces = self.scanFaces(frame)

        CAMERA.setDefaultCameraConfigs()

        return faces

    def saveImage(self, frame, output):
        cv2.imwrite(output, frame)

    def executeCommand(self, command: Command):
        if command.command == "scanFaces":
            self.scanFaces(command.getParameter("frame"))

        if command.command == "getImage":
            self.getImage(command.getParameter("gamma"))

        if command.command == "streamImages":
            self.streamImages()

    def adjustGamma(self, image, gamma=1.0):

        invGamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")

        return cv2.LUT(image, table)

    def streamImages(self):
        while True:
            ref, frame = self.getImage(1.5)
            self.save("frame", frame)
            time.sleep(1 / CAMERA_FPS)


CAMERA_SERVICE = CameraService("CAMERA_SERVICE")

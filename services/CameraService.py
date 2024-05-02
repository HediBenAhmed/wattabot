import time
from typing import List
from drivers.Camera import CAMERA_FPS, CAMERA_HEIGHT, CAMERA_WIDTH, CAMERA
import cv2

from services.Command import Command
from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.Face import Face
from services.JobService import startJobInLoop, stopJobInLoop
from services.Service import Service
from services.SharedData import getSharedData, saveSharedData

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
        return CAMERA.getImage(gamma)

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
            identified = False
            # Check if confidence is less then 40  ==> "0" is perfect match
            if confidence < 49:
                identified = True
                id = NAMES[id]

            confidence = round(100 - confidence)
            faces.append(
                Face(
                    gray[x : x + w, y : y + h],
                    [x, y, w, h],
                    identified,
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

    def startStreaming(self, output: str):
        thread, threadName = CAMERA.streamImages(output)
        self.streamImagesThreadName = threadName

    def stopStreaming(self):
        stopJobInLoop(self.streamImagesThreadName)

    def startScanFaces(self, input: str, output: str):

        def job():
            frame = getSharedData(input)
            faces: List[Face] = self.scanFaces(frame)
            print(faces)
            saveSharedData(output, faces)

        thread, threadName = startJobInLoop(job=job, jobName="scanFaces", delay=1)
        self.scanFacesThreadName = threadName

    def stopScanFaces(self):
        stopJobInLoop(self.scanFacesThreadName)

    def setMaxResolution(self):
        CAMERA.setCameraConfigs(1280, 720)


CAMERA_SERVICE = CameraService("CAMERA_SERVICE")

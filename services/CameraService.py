from typing import List
from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH, CAMERA
import cv2
import numpy as np
from PIL import Image  # pillow package
import os

from services.Command import Command
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

    def scanFaces(self, frame, identifyFace=True):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []

        # Define min window size to be recognized as a face
        minW = int(0.05 * CAMERA.getWidth())
        minH = int(0.05 * CAMERA.getHeight())

        f = FACE_DETECTOR.detectMultiScale(
            image=gray, scaleFactor=1.2, minNeighbors=2, minSize=(minW, minH)
        )

        identified = False
        name, confidence = (None, None)
        for x, y, w, h in f:
            if identifyFace:
                id, confidence = RECONIZER.predict(gray[y : y + h, x : x + w])

                # Check if confidence is less then 40  ==> "0" is perfect match
                if confidence < 49:
                    identified = True
                    name = NAMES[id]

                confidence = round(100 - confidence)
            faces.append(
                Face(
                    gray[y : y + h, x : x + w],
                    [x, y, w, h],
                    identified,
                    name,
                    confidence,
                )
            )

        return faces

    def getImagesAndLabels(self, path):

        imagePaths = [
            os.path.join(path + "/data", f) for f in os.listdir(path + "/data")
        ]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert("L")  # convert it to grayscale
            img_numpy = np.array(PIL_img, "uint8")

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = FACE_DETECTOR.detectMultiScale(img_numpy)

            for x, y, w, h in faces:
                faceSamples.append(img_numpy[y : y + h, x : x + w])
                ids.append(id)

        return faceSamples, ids

    def trainModel(self, pasth, faces, ids):
        RECONIZER.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        RECONIZER.write("trainer/trainer.yml")

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

    def setDefaultCameraConfigs(self):
        CAMERA.setDefaultCameraConfigs()


CAMERA_SERVICE = CameraService("CAMERA_SERVICE")

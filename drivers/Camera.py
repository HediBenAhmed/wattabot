import time
from typing import List
from drivers.Device import Device
import cv2
from services.Configurations import cameraConfig

FACE_DETECTOR = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
RECONIZER = cv2.face.LBPHFaceRecognizer_create()
RECONIZER.read("/home/hedi/wattabot/trainer/trainer.yml")  # load trained model

NAMES = [
    "",
    "hedi",
]  # key in names, start from the second place, leave first empty

CAMERA_FPS = cameraConfig("FPS")
CAMERA_WIDTH = cameraConfig("WIDTH")
CAMERA_HEIGHT = cameraConfig("HEIGHT")


class Camera(Device):
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(cameraConfig("INDEX"))
        self.setCameraConfigs(width, height)

    def saveImage(self, output: str):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(output, frame)

    def read(self):
        return self.cap.read()

    def getFaces(self):
        ret, frame = self.cap.read()
        if not ret:
            return []

        return self.identifyFaces(frame)

    def getImageForStream(self, identifyFaces=False, compress=10):
        ret, frame = self.cap.read()
        if not ret:
            return

        faces: List[Face] = []

        if identifyFaces:

            faces = self.identifyFaces(frame)

            for face in faces:
                x, y, w, h = face.position
                confidence = "  {0}%".format(face.confidence)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                cv2.putText(
                    frame,
                    face.name,
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    confidence,
                    (x + 5, y + h - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 0),
                    1,
                )

        ret, buffer = cv2.imencode(
            ".jpeg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), compress]
        )
        return buffer.tobytes(), faces

    def getImage(self, identifyFaces=False):
        ret, frame = self.cap.read()
        if not ret:
            return

        if identifyFaces:
            faces: List[Face] = self.identifyFaces(frame)

        return frame, faces

    def identifyFaces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = []

        for x, y, w, h in FACE_DETECTOR.detectMultiScale(gray, 1.1, 5):
            id, confidence = RECONIZER.predict(gray[y : y + h, x : x + w])
            # Check if confidence is less them 100 ==> "0" is perfect match
            if confidence < 40:
                id = NAMES[id]
                confidence = round(100 - confidence)
            else:
                id = "unknown"
                confidence = round(100 - confidence)

            faces.append(
                Face(
                    gray[x : x + w, y : y + h],
                    [x, y, w, h],
                    id,
                    confidence,
                )
            )

        return faces

    def setCameraConfigs(self, width: int, heigth: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigth)
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


class Face:
    def __init__(self, image, position: cv2.typing.Rect, name: str, confidence: float):
        self.image = image
        self.position = position
        self.name = name
        self.confidence = confidence


CAMERA = Camera(CAMERA_WIDTH, CAMERA_HEIGHT)

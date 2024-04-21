import time
from typing import List

from drivers.Camera import CAMERA_FPS, CAMERA_HEIGHT, CAMERA_WIDTH, CAMERA
from drivers.Servo import CAMERA_SERVO_H, CAMERA_SERVO_V
import threading
import cv2

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


class CameraService:
    def __init__(self):
        self.moveCamera = False

    def moveLoop(self, x, y, delay=0):
        self.moveCamera = True
        while self.moveCamera:
            self.move(x, y)
            time.sleep(delay)

    def stop(self):
        self.moveCamera = False

    def reset(self):
        CAMERA_SERVO_H.setValue(0)
        CAMERA_SERVO_V.setValue(0)

    def move(self, hStep, vStep):
        h = threading.Thread(target=CAMERA_SERVO_H.move, args=(hStep / 100,))
        v = threading.Thread(target=CAMERA_SERVO_V.move, args=(vStep / 100,))

        h.start()
        v.start()
        h.join()
        v.join()

    def getImage(self):
        return CAMERA.getImage()

    def getImageStream(self, enableFaces=True, identifyFaces=True, compress=10):
        ret, frame = CAMERA.getImage()
        if not ret:
            return

        faces: List[Face] = []

        if enableFaces:
            faces = self.scanFaces(frame, identifyFaces)
            for face in faces:
                x, y, w, h = face.position

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if face.identified:
                    cv2.putText(
                        frame,
                        face.name,
                        (x + 5, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                    )

                    confidence = "  {0}%".format(face.confidence)
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

    def scanFaces(self, frame, identifyFaces=True):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []
        f = FACE_DETECTOR.detectMultiScale(
            image=gray, scaleFactor=1.2, minNeighbors=2, minSize=(30, 30)
        )
        for x, y, w, h in f:
            id = None
            confidence = None
            if identifyFaces:
                id, confidence = RECONIZER.predict(gray[y : y + h, x : x + w])
                # Check if confidence is less then 40  ==> "0" is perfect match
                if confidence < 40:
                    id = NAMES[id]
                else:
                    id = "unknown"

                confidence = round(100 - confidence)
            faces.append(
                Face(
                    gray[x : x + w, y : y + h],
                    [x, y, w, h],
                    identifyFaces,
                    id,
                    confidence,
                )
            )

        return faces

    def centralizeFace(self, face):
        moveTo = self.refFromCameraCenter(face.position)
        self.move(2 * moveTo[0], 2 * moveTo[1])

        return moveTo

    def refFromCameraCenter(self, facePosition):
        x, y, w, h = facePosition
        faceCenter = [x + w / 2, y + h / 2]
        direction = [0, 0]
        hDiff = faceCenter[0] - CENTER_OF_CAMERA[0]
        if abs(hDiff) < CENTER_MARGIN[0]:
            direction[0] = 0
        elif hDiff < 0:
            direction[0] = 1
        elif hDiff > 0:
            direction[0] = -1

        vDiff = faceCenter[1] - CENTER_OF_CAMERA[1]
        if abs(vDiff) < CENTER_MARGIN[1]:
            direction[1] = 0
        elif vDiff < 0:
            direction[1] = -1
        elif vDiff > 0:
            direction[1] = 1

        return direction

    def lookupForFaces(self):
        CAMERA_SERVO_H.setValue(-1)
        CAMERA_SERVO_V.setValue(-1)
        time.sleep(1)

        while True:
            self.move(2, 2)
            time.sleep(2 / CAMERA_FPS)
            ret, frame = CAMERA.getImage()
            if ret:
                faces = self.scanFaces(frame, False)

                if len(faces) > 0:
                    break

        CAMERA.saveImage("out.jpg")

    def saveImage(self, frame, output):
        cv2.imwrite(output, frame)


class Face:
    def __init__(
        self,
        image,
        position: cv2.typing.Rect,
        identified: bool,
        name: str,
        confidence: float,
    ):
        self.image = image
        self.position = position
        self.identified = identified
        if identified:
            self.name = name
            self.confidence = confidence


CAMERA_SERVICE = CameraService()

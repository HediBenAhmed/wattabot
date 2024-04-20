from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH, CAMERA, Face
from drivers.Servo import CAMERA_SERVO_H, CAMERA_SERVO_V
import threading

CENTER_OF_CAMERA = [CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2]
CENTER_MARGIN = [50, 50]


class CameraService:
    def __init__(self):
        self.moveCamera = False

    def up(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(0, -1)

    def down(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(0, 1)

    def left(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(-1, 0)

    def right(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(1, 0)

    def up_left(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(-1, -1)

    def up_right(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(1, -1)

    def down_left(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(-1, 1)

    def down_right(self):
        self.moveCamera = True
        while self.moveCamera:
            self.move(1, 1)

    def stop(self):
        self.moveCamera = False

    def reset(self):
        CAMERA_SERVO_H.setValue(0)
        CAMERA_SERVO_V.setValue(0)

    def move(self, x, y):
        h = threading.Thread(target=CAMERA_SERVO_H.move, args=(x / 100,))
        v = threading.Thread(target=CAMERA_SERVO_V.move, args=(y / 100,))

        h.start()
        v.start()
        h.join()
        v.join()

    def getImageStream(self, identifyFaces=True):
        return CAMERA.getImageForStream(identifyFaces)

    def getImage(self):
        frame, faces = CAMERA.getImage(identifyFaces=True)

        if len(faces) > 0:
            self.centralizeFace(faces[0])

        return frame, faces

    def centralizeFace(self, face: Face):
        moveTo = self.refFromCameraCenter(face.position)
        self.move(2 * moveTo[0], 2 * moveTo[1])

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


CAMERA_SERVICE = CameraService()

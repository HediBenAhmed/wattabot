from drivers.Device import Device
import cv2

FACE_DETECTOR = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


class Camera(Device):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def saveImage(self, output: str):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(output, frame)

    def getImage(self, faceDetect=True):
        ret, frame = self.cap.read()
        if not ret:
            return

        if faceDetect:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = []

            for x, y, w, h in FACE_DETECTOR.detectMultiScale(gray, 1.3, 5):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        ret, buffer = cv2.imencode(".jpeg", frame)
        return buffer.tobytes()

    def setCameraResolution(self, width: int, heigth: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigth)

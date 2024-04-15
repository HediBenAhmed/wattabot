from drivers.Device import Device
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


class Camera(Device):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.setCameraResolution(640, 480)

    def saveImage(self, output: str):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(output, frame)

    def getImage(self, detectFaces=True, identifyFaces=True, compress=20):
        ret, frame = self.cap.read()
        if not ret:
            return

        if detectFaces:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            for x, y, w, h in FACE_DETECTOR.detectMultiScale(gray, 1.3, 5):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if identifyFaces:
                    id, confidence = RECONIZER.predict(gray[y : y + h, x : x + w])
                    # Check if confidence is less them 100 ==> "0" is perfect match
                    if confidence < 40:
                        id = NAMES[id]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        id = "unknown"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        confidence = "  {0}%".format(round(100 - confidence))

                    cv2.putText(
                        frame,
                        str(id),
                        (x + 5, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                    )
                    cv2.putText(
                        frame,
                        str(confidence),
                        (x + 5, y + h - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0),
                        1,
                    )

        ret, buffer = cv2.imencode(
            ".jpeg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), compress]
        )
        return buffer.tobytes()

    def setCameraResolution(self, width: int, heigth: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigth)

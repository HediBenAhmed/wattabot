from time import sleep
from drivers.Camera import CAMERA_FPS
from drivers.Servo import SERVO_MIN_VALUE
from services.CameraService import CameraService
from services.CameraServoService import CameraServoService
from services.Face import Face
from services.LEDService import LEDService
from drivers.LED import matrix_deny
from services.PrivateApiService import PrivateApiService
from services.Service import Service


class IdentificationService(Service):
    def __init__(self):
        self.CAMERA_SERVICE: CameraService = CameraService.getInsance()
        self.CAMERA_SERVO_SERVICE: CameraServoService = CameraServoService.getInsance()
        self.LED_SERVICE: LEDService = LEDService.getInsance()
        self.PRIVATE_API_SERVICE: PrivateApiService = PrivateApiService.getInsance()

    def lookupForFaces(self, horizentalScan=False, verticalScan=True, gamma=1):

        self.CAMERA_SERVO_SERVICE.setPosition(
            SERVO_MIN_VALUE if horizentalScan else 0,
            SERVO_MIN_VALUE if verticalScan else 0,
        )

        faces = []
        identified = None
        while (
            identified is None
            and not self.CAMERA_SERVO_SERVICE.isVerticalMax()
            and not self.CAMERA_SERVO_SERVICE.isHorizentalMax()
        ):

            self.CAMERA_SERVO_SERVICE.move(
                hStep=2 if horizentalScan else 0, vStep=2 if verticalScan else 0
            )

            sleep(2 / CAMERA_FPS)
            ret, frame = self.CAMERA_SERVICE.getImage(gamma)

            faces = self.CAMERA_SERVICE.scanFaces_dnn(frame)
            faces = self.CAMERA_SERVICE.identifyFaces_dnn(faces)

            identified = self.CAMERA_SERVICE.getIdentifiedFace(faces)
            if identified is not None:
                return identified

        return identified

    def identification(self):
        self.LED_SERVICE.clear()

        face: Face = self.lookupForFaces(horizentalScan=False, verticalScan=True)
        if face is None:
            face = self.lookupForFaces(horizentalScan=True, verticalScan=False)

        if face is None:
            self.LED_SERVICE.display(matrix_deny)
        else:
            print(face.name, face.confidence)
            user = self.PRIVATE_API_SERVICE.getUserByName(face.name)

            self.LED_SERVICE.displayName(user.username)

            return user

    @classmethod
    def createInstance(self):
        return IdentificationService()

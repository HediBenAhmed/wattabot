from time import sleep
from drivers.Camera import CAMERA_FPS
from services.BodyIdentifierService import BodyIdentifierService
from services.CameraService import CameraService
from services.CameraServoService import CameraServoService
from services.Face import Face
from services.FaceClassifierService import FaceClassfifierService
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
        self.FACE_SERVICE: FaceClassfifierService = FaceClassfifierService.getInsance()
        self.BODY_SERVICE: BodyIdentifierService = BodyIdentifierService.getInsance()

    def lookupForFace(self):

        self.CAMERA_SERVO_SERVICE.setPosition(0, 0)

        centalizedFace = False

        while not centalizedFace:

            sleep(2 / CAMERA_FPS)
            ret, frame = self.CAMERA_SERVICE.getImage()

            keypoints = self.BODY_SERVICE.reconizeBody_tf(frame)
            nosePoint = self.BODY_SERVICE.getNosePoint(keypoints)

            if nosePoint is not None:
                h, v = CameraServoService.getInsance().centralizeFace2(nosePoint)
                if h == 0 and v == 0:
                    centalizedFace = True

        faces = []
        identified = None

        faces = self.FACE_SERVICE.idenfiyFaces(frame)
        faces = self.FACE_SERVICE.reconizeFaces_dnn(faces)

        identified = self.FACE_SERVICE.getIdentifiedFace(faces)

        return identified

    def identification(self):
        self.LED_SERVICE.clear()

        face: Face = self.lookupForFace()

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

from time import sleep
from typing import List
from drivers.Camera import CAMERA_FPS
from drivers.Servo import SERVO_MIN_VALUE
from services.CameraService import CAMERA_SERVICE
from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.Face import Face
from services.LEDService import LED_SERVICE
from drivers.LED import matrix_deny, matrix_allow


def lookupForFaces(horizentalScan=False, verticalScan=True):
    CAMERA_SERVO_SERVICE.setPosition(
        SERVO_MIN_VALUE if horizentalScan else 0, SERVO_MIN_VALUE if verticalScan else 0
    )

    faces = []
    identified = None
    while (
        identified is None
        and not CAMERA_SERVO_SERVICE.isVerticalMax()
        and not CAMERA_SERVO_SERVICE.isHorizentalMax()
    ):

        CAMERA_SERVO_SERVICE.move(
            hStep=2 if horizentalScan else 0, vStep=2 if verticalScan else 0
        )

        sleep(2 / CAMERA_FPS)
        ret, frame = CAMERA_SERVICE.getImage(1.5)

        faces = CAMERA_SERVICE.scanFaces(frame)

        identified = getIdentifiedFaces(faces)
        if identified is not None:
            return identified

    return identified


def getIdentifiedFaces(faces: List[Face]):
    if faces is None:
        return None

    for face in faces:
        if face.identified:
            return face

    return None


if __name__ == "__main__":
    LED_SERVICE.clear()
    CAMERA_SERVICE.setMaxResolution()

    face: Face = lookupForFaces(horizentalScan=False, verticalScan=True)
    if face is None:
        dace = lookupForFaces(horizentalScan=True, verticalScan=False)

    if face is None:
        LED_SERVICE.display(matrix_deny)
    else:
        print(face.name)
        LED_SERVICE.display(matrix_allow)
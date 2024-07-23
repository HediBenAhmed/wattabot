from services.Service import Service
from tflite_runtime.interpreter import Interpreter
import cv2


class BodyIdentifierService(Service):
    def __init__(self):
        self.input_details = None
        self.output_details = None
        self.interpreter = None

    def initTf(self):
        if self.interpreter is None:
            # Load TFLite model and allocate tensors.
            self.interpreter = Interpreter(
                model_path="/home/hedi/wattabot/models/simple_pose_model.tflite"
            )

            # Get input and output tensors.
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()

            self.interpreter.allocate_tensors()

    def reconizeBody_tf(self, image):
        self.initTf()
        new_img = cv2.resize(image, (192, 192))

        # input_details[0]['index'] = the index which accepts the input
        self.interpreter.set_tensor(self.input_details[0]["index"], [new_img])

        # run the inference
        self.interpreter.invoke()

        # output_details[0]['index'] = the index which provides the input

        keypoints_with_scores = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )

        imgheight, imgwidth, _ = image.shape
        kpts_absolute_xy = []
        for i in range(17):
            kpt_x = keypoints_with_scores[0, 0, i, 1]
            kpt_y = keypoints_with_scores[0, 0, i, 0]
            kpt_score = keypoints_with_scores[0, 0, i, 2]

            kpts_absolute_xy.append(
                [
                    imgwidth * kpt_x,
                    imgheight * kpt_y,
                    kpt_score >= MIN_CROP_KEYPOINT_SCORE,
                    kpt_score,
                ]
            )

        return kpts_absolute_xy

    def getNosePoint(self, keypoints):
        nosePoint = keypoints[KEYPOINT_DICT["nose"]]

        if nosePoint[2]:
            return nosePoint

        left_shoulderPoint = keypoints[KEYPOINT_DICT["left_shoulder"]]
        right_shoulderPoint = keypoints[KEYPOINT_DICT["right_shoulder"]]
        left_hipPoint = keypoints[KEYPOINT_DICT["left_hip"]]
        right_hipPoint = keypoints[KEYPOINT_DICT["right_hip"]]
        left_kneePoint = keypoints[KEYPOINT_DICT["left_knee"]]
        right_kneePoint = keypoints[KEYPOINT_DICT["right_knee"]]

        if (
            left_shoulderPoint[2]
            or right_shoulderPoint[2]
            or left_hipPoint[2]
            or right_hipPoint[2]
            or left_kneePoint[2]
            or right_kneePoint[2]
        ):
            return nosePoint

    @classmethod
    def createInstance(self):
        return BodyIdentifierService()


# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    "nose": 0,
    "left_eye": 1,
    "right_eye": 2,
    "left_ear": 3,
    "right_ear": 4,
    "left_shoulder": 5,
    "right_shoulder": 6,
    "left_elbow": 7,
    "right_elbow": 8,
    "left_wrist": 9,
    "right_wrist": 10,
    "left_hip": 11,
    "right_hip": 12,
    "left_knee": 13,
    "right_knee": 14,
    "left_ankle": 15,
    "right_ankle": 16,
}

MIN_CROP_KEYPOINT_SCORE = 0.5

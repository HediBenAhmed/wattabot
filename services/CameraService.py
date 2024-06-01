import pickle
from typing import List
from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH, Camera
import cv2
import numpy as np
from PIL import Image
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from services.Face import Face
from services.Service import Service

FACE_DETECTOR = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
RECONIZER = cv2.face.LBPHFaceRecognizer_create()
RECONIZER.read("/home/hedi/wattabot/trainer/trainer.yml")  # load trained model

NAMES = [
    "",
    "hedi",
]  # key in names, start from the second place, leave first empty


FACE_DETECTOR_DNN = cv2.dnn.readNetFromCaffe(
    "/home/hedi/wattabot/face_detection_model/deploy.prototxt",
    "/home/hedi/wattabot/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel",
)

EMBEDDER_DNN = cv2.dnn.readNetFromTorch(
    "/home/hedi/wattabot/face_detection_model/openface_nn4.small2.v1.t7"
)

CENTER_OF_CAMERA = [CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2]
CENTER_MARGIN = [50, 50]


class CameraService(Service):

    def __init__(self):
        self.CAMERA = Camera(CAMERA_WIDTH, CAMERA_HEIGHT)

    def getImage(self, gamma=1.0):
        ret, frame = self.CAMERA.getImage(gamma)
        return ret, frame

    def scanFaces_haar(self, frame, identifyFace=True):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []

        # Define min window size to be recognized as a face
        minW = int(0.05 * self.CAMERA.getWidth())
        minH = int(0.05 * self.CAMERA.getHeight())

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

    def scanFaces_dnn(self, frame):
        # grab the image dimensions
        h, w = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False
        )

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        FACE_DETECTOR_DNN.setInput(imageBlob)
        detections = FACE_DETECTOR_DNN.forward()
        faces = []
        # loop over the detections
        for i in range(0, detections.shape[2]):

            # extract the confidence (i.e., probability) associated with
            # the prediction
            # filter out weak detections
            if detections[0, 0, i, 2] > 0.80:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]

                faces.append(
                    Face(
                        face,
                        [startX, startY, endX - startX, endY - startY],
                        False,
                        None,
                        None,
                    )
                )

        return faces

    def identifyFaces_dnn(self, faces: List[Face]):
        database = pickle.loads(
            open(
                "/home/hedi/wattabot/face_detection_model/embeddings.pickle", "rb"
            ).read()
        )

        for face in faces:
            self.identifyFace_dnn(face, database)

        return faces

    def identifyFace_dnn(self, face: Face, database):
        # grab the image dimensions
        (fH, fW) = face.image.shape[:2]
        # ensure the face width and height are sufficiently large
        if fW < 20 or fH < 20:
            return face

        # construct a blob for the face ROI, then pass the blob
        # through our face embedding model to obtain the 128-d
        # quantification of the face
        faceBlob = cv2.dnn.blobFromImage(
            face.image,
            1.0 / 255,
            (96, 96),
            (0, 0, 0),
            swapRB=True,
            crop=False,
        )
        EMBEDDER_DNN.setInput(faceBlob)
        vec = EMBEDDER_DNN.forward()

        # perform classification to recognize the face
        similarity, name = self.whoIsIt(vec, database)
        confidence = round(100 - similarity * 100)

        face.identified = name is not None and confidence > 50
        if face.identified:
            face.name = name
            face.confidence = confidence

        return face

    def whoIsIt(self, vector, database):
        encoding = vector
        min_dist = 100
        identity = None
        for i in range(len(database["embeddings"])):
            db_enc = database["embeddings"][i]
            name = database["names"][i]
            dist = np.linalg.norm(encoding - db_enc)

            if dist < min_dist:
                min_dist = dist
                identity = name
        if not min_dist < 0.55:
            identity = None
        return min_dist, identity

    def getImagesAndLabels_haar(self, path):

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

    def trainModel_haar(self, faces, ids):
        RECONIZER.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        RECONIZER.write("trainer/trainer.yml")

    def trainModel_dnn(self, path):
        imagePaths = []
        for root, dirs, files in os.walk(path + "/data"):
            for file in files:
                imagePaths.append(os.path.join(root, file))

        knownEmbeddings = []
        knownNames = []

        # loop over the image paths
        for imagePath in imagePaths:

            name = imagePath.split(os.path.sep)[-2]

            face = cv2.imread(imagePath)

            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv2.dnn.blobFromImage(
                face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False
            )
            EMBEDDER_DNN.setInput(faceBlob)
            vec = EMBEDDER_DNN.forward()

            # add the name of the person + corresponding face
            # embedding to their respective lists
            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())

        # dump the facial embeddings + names to disk
        data = {"embeddings": knownEmbeddings, "names": knownNames}
        f = open("/home/hedi/wattabot/face_detection_model/embeddings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()

        le = LabelEncoder()
        labels = le.fit_transform(data["names"])

        # train the model used to accept the 128-d embeddings of the face and
        # then produce the actual face recognition
        recognizer = SVC(C=2, kernel="rbf", probability=True)
        recognizer.fit(data["embeddings"], labels)

        f = open("/home/hedi/wattabot/face_detection_model/model.pickle", "wb")
        f.write(pickle.dumps(recognizer))
        f.close()

        # write the label encoder to disk
        f = open("/home/hedi/wattabot/face_detection_model/label_encoder.pickle", "wb")
        f.write(pickle.dumps(le))
        f.close()

    def saveImage(self, frame, output):
        cv2.imwrite(output, frame)

    def setMaxResolution(self):
        self.CAMERA.setCameraConfigs(1280, 720)

    def setDefaultCameraConfigs(self):
        self.CAMERA.setDefaultCameraConfigs()

    def getIdentifiedFace(self, faces: List[Face]):
        if faces is None:
            return None

        for face in faces:
            if face.identified:
                return face

        return None

    @classmethod
    def createInstance(self):
        return CameraService()

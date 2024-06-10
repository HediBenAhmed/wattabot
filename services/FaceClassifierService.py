from typing import List
from services.Face import Face
from services.Service import Service
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle


class FaceClassfifierService(Service):
    def __init__(self):
        self.labels = None
        self.input_details = None
        self.output_details = None
        self.interpreter = None

        self.faceDetector = None
        self.database_dnn = None
        self.embedder_dnn = None

    def initTf(self):
        if self.interpreter is None:
            with open("/home/hedi/wattabot/models/labels.txt", "r") as f:
                self.labels = [line.strip() for line in f.readlines()]

            # Load TFLite model and allocate tensors.
            self.interpreter = Interpreter(
                model_path="/home/hedi/wattabot/models/model_int8.tflite"
            )

            # Get input and output tensors.
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()

            self.interpreter.allocate_tensors()

    def initFaceDetector(self):
        if self.faceDetector is None:
            self.faceDetector = cv2.dnn.readNetFromCaffe(
                "/home/hedi/wattabot/models/deploy.prototxt",
                "/home/hedi/wattabot/models/res10_300x300_ssd_iter_140000.caffemodel",
            )

    def initEmbedder_dnn(self):
        if self.embedder_dnn is None:
            self.embedder_dnn = cv2.dnn.readNetFromTorch(
                "/home/hedi/wattabot/models/openface_nn4.small2.v1.t7"
            )

    def initDatabse_dnn(self):
        if self.database_dnn is None:
            self.database_dnn = pickle.loads(
                open("/home/hedi/wattabot/models/embeddings.pickle", "rb").read()
            )

    def reconizeFace_tf(self, image):
        self.initTf()
        new_img = cv2.resize(image, (300, 300))

        # input_details[0]['index'] = the index which accepts the input
        self.interpreter.set_tensor(self.input_details[0]["index"], [new_img])

        # run the inference
        self.interpreter.invoke()

        # output_details[0]['index'] = the index which provides the input

        detection_boxes = self.interpreter.get_tensor(self.output_details[0]["index"])

        result = np.squeeze(detection_boxes)

        top_k = np.argsort(result)[::-1][0]

        return self.labels[top_k], float(result[top_k] / 2.55)

    def reconizeFaces_tf(self, faces: List[Face]):
        for face in faces:
            name, confidence = self.reconizeFace_tf(face.image)
            if confidence > 55:
                face.name = name
                face.confidence = confidence
                face.identified = True
        return faces

    def idenfiyFaces(self, frame):
        self.initFaceDetector()
        # grab the image dimensions
        h, w = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False
        )

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        self.faceDetector.setInput(imageBlob)
        detections = self.faceDetector.forward()
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

    def reconizeFaces_dnn(self, faces: List[Face]):
        for face in faces:
            self.reconizeFace_dnn(face)

        return faces

    def reconizeFace_dnn(self, face: Face):
        self.initEmbedder_dnn()
        self.initDatabse_dnn()
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
        self.embedder_dnn.setInput(faceBlob)
        vec = self.embedder_dnn.forward()

        # perform classification to recognize the face
        similarity, name = self.whoIsIt(vec, self.database_dnn)
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

    def trainModel_dnn(self):
        self.initEmbedder_dnn()
        imagePaths = []
        for root, dirs, files in os.walk("/home/hedi/wattabot/trainer/data"):
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
            self.embedder_dnn.setInput(faceBlob)
            vec = self.embedder_dnn.forward()

            # add the name of the person + corresponding face
            # embedding to their respective lists
            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())

        # dump the facial embeddings + names to disk
        data = {"embeddings": knownEmbeddings, "names": knownNames}
        f = open("/home/hedi/wattabot/models/embeddings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()

        le = LabelEncoder()
        labels = le.fit_transform(data["names"])

        # train the model used to accept the 128-d embeddings of the face and
        # then produce the actual face recognition
        recognizer = SVC(C=2, kernel="rbf", probability=True)
        recognizer.fit(data["embeddings"], labels)

        f = open("/home/hedi/wattabot/models/model.pickle", "wb")
        f.write(pickle.dumps(recognizer))
        f.close()

        # write the label encoder to disk
        f = open("/home/hedi/wattabot/models/label_encoder.pickle", "wb")
        f.write(pickle.dumps(le))
        f.close()

    def getIdentifiedFace(self, faces: List[Face]):
        if faces is None:
            return None

        for face in faces:
            if face.identified:
                return face

        return None

    @classmethod
    def createInstance(self):
        return FaceClassfifierService()

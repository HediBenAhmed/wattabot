import cv2


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
        self.name = name
        self.confidence = confidence

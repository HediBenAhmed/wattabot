from typing import List


class Object:
    def __init__(self, position: float, distance: float):
        self.positions = [position]
        self.distance = round(distance, 0)

    def addPosition(self, position: float):
        self.positions.append(position)

    def __str__(self):
        return f"Object('{self.distance}', {self.positions})"


def geObjectByDistance(objects: List[Object], distance: float):
    distance = round(distance, 0)
    for object in objects:
        if object.distance == distance:
            return object

    return None

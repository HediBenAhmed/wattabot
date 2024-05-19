from drivers.LED import *
from services.Service import Service

NAMES_MATRIX = {"hedi": matrix_hedi, "saida": matrix_dida}


class LEDService(Service):

    def display(self, matrix):
        LED_SCREEN.matrix_display(matrix)

    def clear(self):
        LED_SCREEN.matrix_display(off)

    def displayName(self, name):
        LED_SCREEN.matrix_display(NAMES_MATRIX[name])

    @classmethod
    def createInstance(self):
        return LEDService()

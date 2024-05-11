from drivers.LED import *
from services.Service import Service


class LEDService(Service):

    def display(self, matrix):
        LED_SCREEN.matrix_display(matrix)

    def clear(self):
        LED_SCREEN.matrix_display(off)


LED_SERVICE = LEDService()

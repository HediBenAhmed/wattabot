from drivers.LED import LED_SCREEN, matrix_hedi, matrix_forward, off
from services.Service import Service


class LEDService(Service):

    def display(self, matrix):
        LED_SCREEN.matrix_display(matrix)

    def clear(self):
        LED_SCREEN.matrix_display(off)


LED_SERVICE = LEDService("LED_SERVICE")

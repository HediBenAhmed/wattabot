from drivers.LED import LED_SCREEN, matrix_hedi, matrix_forward, off
from services.Service import Service


class LEDService(Service):

    def __init__(self):
        super().__init__("LED_SERVICE")

    def display(self):
        LED_SCREEN.matrix_display(matrix_forward)

    def clear(self):
        LED_SCREEN.matrix_display(off)


LED_SERVICE = LEDService()

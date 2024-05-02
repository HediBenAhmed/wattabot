from services.Configurations import connectorConfig
from drivers.Device import Device
import time
import RPi.GPIO as GPIO

# Display pattern data
off = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
)
smile = (
    0x00,
    0x00,
    0x38,
    0x40,
    0x40,
    0x40,
    0x3A,
    0x02,
    0x02,
    0x3A,
    0x40,
    0x40,
    0x40,
    0x38,
    0x00,
    0x00,
)
matrix_forward = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x12,
    0x24,
    0x48,
    0x90,
    0x90,
    0x48,
    0x24,
    0x12,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_back = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x48,
    0x24,
    0x12,
    0x09,
    0x09,
    0x12,
    0x24,
    0x48,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_left = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x18,
    0x24,
    0x42,
    0x99,
    0x24,
    0x42,
    0x81,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_right = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x81,
    0x42,
    0x24,
    0x99,
    0x42,
    0x24,
    0x18,
    0x00,
    0x00,
    0x00,
    0x00,
)

matrix_dida = (
    0x7C,
    0x44,
    0x44,
    0x38,
    0x00,
    0x7C,
    0x00,
    0x7C,
    0x44,
    0x44,
    0x38,
    0x00,
    0x78,
    0x14,
    0x14,
    0x78,
)

matrix_hedi = (
    0x7E,
    0x10,
    0x10,
    0x7E,
    0x00,
    0x7E,
    0x52,
    0x52,
    0x00,
    0x7E,
    0x42,
    0x42,
    0x3C,
    0x00,
    0x7E,
    0x00,
)

matrix_deny = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x42,
    0x24,
    0x18,
    0x18,
    0x24,
    0x42,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
)

matrix_allow = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x08,
    0x10,
    0x20,
    0x40,
    0x20,
    0x10,
    0x08,
    0x04,
    0x02,
    0x00,
    0x00,
    0x00,
)


class LED(Device):
    def __init__(self):
        self.SCLK = connectorConfig("LED_SCLK")
        self.DIO = connectorConfig("LED_DIO")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.SCLK, GPIO.OUT)
        GPIO.setup(self.DIO, GPIO.OUT)

    def nop(self):
        time.sleep(0.00003)

    def start(self):
        GPIO.output(self.SCLK, 0)
        self.nop()
        GPIO.output(self.SCLK, 1)
        self.nop()
        GPIO.output(self.DIO, 1)
        self.nop()
        GPIO.output(self.DIO, 0)
        self.nop()

    def matrix_clear(self):
        self.matrix_display(off)
        GPIO.output(self.SCLK, 0)
        self.nop()
        GPIO.output(self.DIO, 0)
        self.nop()
        GPIO.output(self.DIO, 0)
        self.nop()

    def send_date(self, date):
        for i in range(0, 8):
            GPIO.output(self.SCLK, 0)
            self.nop()
            if date & 0x01:
                GPIO.output(self.DIO, 1)
            else:
                GPIO.output(self.DIO, 0)
            self.nop()
            GPIO.output(self.SCLK, 1)
            self.nop()
            date >>= 1
            GPIO.output(self.SCLK, 0)

    def end(self):
        GPIO.output(self.SCLK, 0)
        self.nop()
        GPIO.output(self.DIO, 0)
        self.nop()
        GPIO.output(self.SCLK, 1)
        self.nop()
        GPIO.output(self.DIO, 1)
        self.nop()

    def matrix_display(self, matrix_value):
        self.start()
        self.send_date(0xC0)

        for i in range(0, 16):
            self.send_date(matrix_value[i])

        self.end()
        self.start()
        self.send_date(0x8A)
        self.end()


LED_SCREEN = LED()

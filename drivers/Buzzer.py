import time
from drivers.Device import Device
from services.Configurations import connectorConfig
import RPi.GPIO as GPIO

# Happy birthday
Do = 262
Re = 294
Mi = 330
Fa = 349
Sol = 392
La = 440
Si = 494
Do_h = 523
Re_h = 587
Mi_h = 659
Fa_h = 698
Sol_h = 784
La_h = 880
Si_h = 988


class Buzzer(Device):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pin = connectorConfig("BUZZER")
        GPIO.setup(pin, GPIO.OUT)
        self.buzz = GPIO.PWM(pin, 440)

    def beep(self, frequency: float, delay: float = 1):
        self.buzz.start(50)
        self.buzz.ChangeFrequency(frequency)  # Change the frequency along the song note
        time.sleep(delay)  # delay a note for beat
        self.buzz.stop()

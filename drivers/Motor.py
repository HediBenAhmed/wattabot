from drivers.Device import Device
import RPi.GPIO as GPIO


class Motor(Device):
    def __init__(self, in1: int, in2: int, pwm: int):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(pwm, GPIO.OUT)

        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)

        self.in1 = in1
        self.in2 = in2
        self.pwm = GPIO.PWM(pwm, 100)

    def goForward(self):
        self.pwm.start(0)
        GPIO.output(self.in2, GPIO.LOW)  # Upper Left forward
        GPIO.output(self.in1, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(50)

    def goBackward(self):
        self.pwm.start(0)
        GPIO.output(self.in2, GPIO.HIGH)  # Upper Left forward
        GPIO.output(self.in1, GPIO.LOW)
        self.pwm.ChangeDutyCycle(50)

    def stop(self):
        self.pwm.stop()

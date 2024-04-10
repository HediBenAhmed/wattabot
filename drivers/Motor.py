import time
from drivers.Device import Device
from gpiozero import Motor as GpMotor
from drivers.Connectors import (
    M1_IN3,
    M1_IN4,
    M2_IN2,
    M2_IN1,
    M3_IN1,
    M3_IN2,
    M4_IN4,
    M4_IN3,
)


class Motor(Device):
    def __init__(self, in1: int, in2: int):
        self.motor = GpMotor(in1, in2)

    def goForward(self, delay: float):
        self.motor.forward()
        time.sleep(delay)
        self.motor.stop()

    def goBackward(self, delay: float):
        self.motor.backward()
        time.sleep(delay)
        self.motor.stop()


MOTOR_M1 = Motor(M1_IN3, M1_IN4)
MOTOR_M2 = Motor(M2_IN2, M2_IN1)
MOTOR_M3 = Motor(M3_IN1, M3_IN2)
MOTOR_M4 = Motor(M4_IN4, M4_IN3)

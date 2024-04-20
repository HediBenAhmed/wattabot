from services.Configurations import connectorConfig
from drivers.Device import Device
import time
import RPi.GPIO as GPIO

KEY_UP = 0x46
KEY_LEFT = 0x44
KEY_OK = 0x40
KEY_RIGHT = 0x43
KEY_DOWN = 0x15
KEY_1 = 0x16
KEY_2 = 0x19
KEY_3 = 0x0D
KEY_4 = 0x0C
KEY_5 = 0x18
KEY_6 = 0x5E
KEY_7 = 0x08
KEY_8 = 0x1C
KEY_9 = 0x5A
KEY_STAR = 0x42
KEY_0 = 0x52
KEY_HASH = 0x4A

IR_PIN = connectorConfig("RECEIVER_IR")


class IrcReceiver(Device):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IR_PIN, GPIO.IN, GPIO.PUD_UP)

    def readKey(self):
        while True:
            if GPIO.input(IR_PIN) == 0:
                count = 0
                while (
                    GPIO.input(IR_PIN) == 0 and count < 200
                ):  # Wait for 9ms LOW level boot code and exit the loop if it exceeds 1.2ms
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while (
                    GPIO.input(IR_PIN) == 1 and count < 80
                ):  # Wait for a 4.5ms HIGH level boot code and exit the loop if it exceeds 0.48ms
                    count += 1
                    time.sleep(0.00006)

                idx = 0  # byte count variable
                cnt = 0  # Variable per byte bit
                # There are 4 bytes in total. The first byte is the address code, the second is the address inverse code,
                # the third is the control command data of the corresponding button, and the fourth is the control command inverse code
                data = [0, 0, 0, 0]
                for i in range(0, 32):  # Start receiving 32BITE data
                    count = 0
                    while (
                        GPIO.input(IR_PIN) == 0 and count < 15
                    ):  # Wait for the LOW LOW level of 562.5US to pass and exit the loop if it exceeds 900US
                        count += 1
                        time.sleep(0.00006)

                    count = 0
                    while (
                        GPIO.input(IR_PIN) == 1 and count < 40
                    ):  # waits for logical HIGH level to pass and exits the loop if it exceeds 2.4ms
                        count += 1
                        time.sleep(0.00006)

                    # if count>8, that is, the logical time is greater than 0.54+0.562=1.12ms, that is,
                    # the period is greater than the logical 0 period, that is equivalent to receiving logical 1
                    if count > 8:
                        data[idx] |= (
                            1 << cnt
                        )  # When idx=0 is the first data  data[idx] = data[idx] | 1<<cnt   00000001 <<1 == 0000 0010
                    if cnt == 7:  # With 8 byte
                        cnt = 0  # Displacement qing 0
                        idx += 1  # Store the next data
                    else:
                        cnt += 1  # The shift adds 1
                # Determine whether address code + address inverse code =0xff, control code + control inverse code = 0xFF
                if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:
                    # Data [2] is the control code we need
                    return data[2]

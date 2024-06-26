from typing import List
from drivers.Device import Device
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 64

margingLeft = 5
margingTop = 5


class OLED(Device):
    def __init__(self):
        # Define the Reset Pin
        oled_reset = digitalio.DigitalInOut(board.D4)
        # Use for I2C.
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset
        )

        # Clear display.
        self.oled.fill(0)
        self.oled.show()

    def displayTexts(self, texts: List[str]):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Load default font.
        font = ImageFont.load_default()
        top = margingTop
        for text in texts:
            draw.text((margingLeft, top), text, font=font, fill=255)
            top += 10

        # Display image
        self.oled.image(image)
        self.oled.show()

    def clear(self):
        # Clear display.
        self.oled.fill(0)
        self.oled.show()

import RPi.GPIO as GPIO
import time
import os

class SMLed:

  def __init__(self, pin_red, pin_green):
    # RPi.GPIO pin number for red and green led control
    self.pins = [pin_red, pin_green]

    # initialise GPIO pins and define as output
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.pins, GPIO.OUT)

    # switch LED to red
    GPIO.output(self.pins, (GPIO.HIGH, GPIO.LOW))

  def __del__(self):
    GPIO.cleanup()

  def red(self):
    GPIO.output(self.pins, (GPIO.HIGH, GPIO.LOW))

  def green(self):
    GPIO.output(self.pins, (GPIO.LOW, GPIO.HIGH))

  def yellow(self):
    GPIO.output(self.pins, (GPIO.HIGH, GPIO.HIGH))

  def off(self):
    GPIO.output(self.pins, (GPIO.LOW, GPIO.LOW))

if __name__ == "__main__":

  led = SMLed(15, 16)

  for i in range(10):
    led.red()
    time.sleep(0.5)
    led.off()
    time.sleep(0.2)
    led.green()
    time.sleep(0.5)
    led.off()
    time.sleep(0.2)
    led.yellow()
    time.sleep(0.5)
    led.off()
    time.sleep(0.2)

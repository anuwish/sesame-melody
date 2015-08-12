import time
import os

class Led:
  # create mockup to develop w/o need for an RasPi
  mockup = True
  try:
    import RPi.GPIO as GPIO
    mockup = False
  except:
    pass

  def __init__(self, pin_red, pin_green):
    # RPi.GPIO pin number for red and green led control
    self.pins = [pin_red, pin_green]

    if not Led.mockup:
      # initialise GPIO pins and define as output
      Led.GPIO.setmode(Led.GPIO.BOARD)
      Led.GPIO.setup(self.pins, Led.GPIO.OUT)
      Led.GPIO.setwarnings(False)

      # switch LED to red
      Led.GPIO.output(self.pins, (Led.GPIO.HIGH, Led.GPIO.LOW))
    else:
      print 'smgpio.visual.mockup', '__init__(self, pin_red, pin_green)'

  def __del__(self):
    if not Led.mockup:
      Led.GPIO.cleanup()
    else:
      print 'smgpio.visual.mockup', '__del__(self)'

  def red(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.HIGH, Led.GPIO.LOW))
    else:
      print 'smgpio.visual.mockup', 'red(self)'

  def green(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.LOW, Led.GPIO.HIGH))
    else:
      print 'smgpio.visual.mockup', 'green(self)'

  def yellow(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.HIGH, Led.GPIO.HIGH))
    else:
      print 'smgpio.visual.mockup', 'yellow(self)'

  def off(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.LOW, Led.GPIO.LOW))
    else:
      print 'smgpio.visual.mockup', 'off(self)'

if __name__ == "__main__":

  led = Led(15, 16)

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

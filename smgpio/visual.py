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
      print 'smgpio.visual.led.mockup', '__init__(self, pin_red, pin_green)'

  def cleanup(self):
    if not Led.mockup:
      Led.GPIO.cleanup()
    else:
      print 'smgpio.visual.led.mockup', 'cleanup(self)'

  def red(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.HIGH, Led.GPIO.LOW))
    else:
      print 'smgpio.visual.led.mockup', 'red(self)'

  def green(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.LOW, Led.GPIO.HIGH))
    else:
      print 'smgpio.visual.led.mockup', 'green(self)'

  def yellow(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.HIGH, Led.GPIO.HIGH))
    else:
      print 'smgpio.visual.led.mockup', 'yellow(self)'

  def off(self):
    if not Led.mockup:
      Led.GPIO.output(self.pins, (Led.GPIO.LOW, Led.GPIO.LOW))
    else:
      print 'smgpio.visual.led.mockup', 'off(self)'

class DotMatrix:
  # create mockup to develop w/o need for an RasPi
  mockup = True
  try:
    import RPi.GPIO as GPIO
    mockup = False
  except:
    pass
  # dot matrix display
  # C for column
  # R for row
  # DMD for internal wiring
  # GPIO pin naming
  # PIN physical numbering
  #
  # C1 = DMD1  = GPIO11 = PIN23
  # C2 = DMD3  = GPIO8  = PIN24
  # C3 = DMD10 = GPIO7  = PIN26
  # C4 = DMD7  = GPIO5  = PIN29
  # C5 = DMD8  = GPIO6  = PIN31
  # R1 = DMD12 = GPIO12 = PIN32
  # R2 = DMD11 = GPIO13 = PIN33
  # R3 = DMD2  = GPIO19 = PIN35
  # R4 = DMD9  = GPIO16 = PIN36
  # R5 = DMD4  = GPIO26 = PIN37
  # R6 = DMD5  = GPIO20 = PIN38
  # R7 = DMD6  = GPIO21 = PIN40

  pinC1 = 23
  pinC2 = 24
  pinC3 = 26
  pinC4 = 29
  pinC5 = 31
  pinR1 = 32
  pinR2 = 33
  pinR3 = 35
  pinR4 = 36
  pinR5 = 37
  pinR6 = 38
  pinR7 = 40
  columns = [pinC1, pinC2, pinC3, pinC4, pinC5]
  rows    = [pinR1, pinR2, pinR3, pinR4, pinR5, pinR6, pinR7]
  pins    = [pinC1, pinC2, pinC3, pinC4, pinC5, pinR1, pinR2, pinR3, pinR4, pinR5, pinR6, pinR7]

  col_dict = {0 : pinC1, 1 : pinC2, 2 : pinC3, 3 : pinC4, 4 : pinC5}
  row_dict = {0 : pinR1, 1 : pinR2, 2 : pinR3, 3 : pinR4, 4 : pinR5, 5 : pinR6, 6 : pinR7}

  def __init__(self):
    if not DotMatrix.mockup:
      # initialise GPIO pins
      DotMatrix.GPIO.setmode(DotMatrix.GPIO.BOARD)
    else:
      print 'smgpio.visual.dotmatrix.mockup', '__init__(self)'

  def cleanup(self):
    if not DotMatrix.mockup:
      DotMatrix.GPIO.cleanup()
    else:
      print 'smgpio.visual.dotmatrix.mockup', 'cleanup(self)'

  def dot_on(self, col, row):
    if not DotMatrix.mockup:
      DotMatrix.GPIO.setup(col, DotMatrix.GPIO.OUT)
      DotMatrix.GPIO.setup(row, DotMatrix.GPIO.OUT)

      DotMatrix.GPIO.output(col, 1)
      DotMatrix.GPIO.output(row, 0)
    else:
      print 'smgpio.visual.dotmatrix.mockup', 'dot_on(self, col, row)'

  def level(self, lvl):
    if not DotMatrix.mockup:
      # active all columns and rows
      DotMatrix.GPIO.setup(DotMatrix.columns, DotMatrix.GPIO.OUT)
      DotMatrix.GPIO.setup(DotMatrix.rows, DotMatrix.GPIO.IN)
      # switch on all columns
      DotMatrix.GPIO.output(DotMatrix.columns, 1)

      # switch on rows for each lvl
      for i in range(lvl):
        DotMatrix.GPIO.setup(DotMatrix.row_dict[i], DotMatrix.GPIO.OUT)
        DotMatrix.GPIO.output(DotMatrix.row_dict[i], 0)
      DotMatrix.GPIO.setmode(DotMatrix.GPIO.BOARD)
    else:
      print 'smgpio.visual.dotmatrix.mockup', 'level(self, lvl)'

  # WIP, ccauet 2015-08-13
  # def pattern_on(self, pattern):
  #   # switch of all pins
  #   DotMatrix.GPIO.setup(DotMatrix.columns, DotMatrix.GPIO.IN)
  #   DotMatrix.GPIO.setup(DotMatrix.rows, DotMatrix.GPIO.IN)

  #   for iteration in range(50):

  #     nr = 0
  #     # loop over rows
  #     for r in pattern:
  #       # activate row
  #       DotMatrix.GPIO.setup(DotMatrix.row_dict[nr], DotMatrix.GPIO.OUT)
  #       DotMatrix.GPIO.output(DotMatrix.row_dict[nr], 0)

  #       # loop over columns
  #       nc = 0
  #       for c in r:
  #         # switch on column
  #         DotMatrix.GPIO.setup(DotMatrix.col_dict[nc], DotMatrix.GPIO.OUT)
  #         DotMatrix.GPIO.output(DotMatrix.col_dict[nc], pattern[nr][nc])

  #         nc = nc + 1

  #       # deactivate row
  #       time.sleep(0.01)
  #       DotMatrix.GPIO.setup(DotMatrix.row_dict[nr], DotMatrix.GPIO.IN)

  #       nr = nr + 1

  #     time.sleep(0.01)


if __name__ == "__main__":

  # dot matrix testing
  dmd = DotMatrix()

  dmd.level(3)
  time.sleep(2)
  dmd.level(5)
  time.sleep(2)
  dmd.level(3)
  time.sleep(2)

  dmd.cleanup()


  # LED testing
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

  led.cleanup()

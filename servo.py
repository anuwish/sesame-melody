import RPi.GPIO as GPIO
import time
import os

class SMServo:

  # the servo is a 'TowerPro SG90' or similar
  # http://www.servodatabase.com/servo/towerpro/sg90
  # with a pulse width of 500-2400 micro-seconds
  # at an PWM base frequency of 50Hz / period of 20ms

  ANGLE_RANGE = 180 # tested, not for sure
  BASE_FREQ = 50
  BASE_PERIOD = 1000.0 * 1/BASE_FREQ
  MIN_PULSE_WIDTH = 0.5
  MAX_PULSE_WIDTH = 2.4 
  MIN_POS = 100.0 * MIN_PULSE_WIDTH/BASE_PERIOD
  MAX_POS = 100.0 * MAX_PULSE_WIDTH/BASE_PERIOD
  OPEN_POS = 180
  CLOSE_POS = 0
  NEUTRAL_POS = 0.5 * (MAX_POS + MIN_POS)

  T_PER_60 = 0.17 # tested, not for sure
  T_MAX = ANGLE_RANGE/60.0 * T_PER_60

  def __init__(self, pin, init_pos):
    # GPIO PWN pin number
    self.pin = pin
    # log current position as hardware feedback is not possible
    # thus, an initialisation value is necessary
    self.pos = init_pos

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.pin, GPIO.OUT)

    # initialise GPIO.PWM servo instance
    self.servo = GPIO.PWM(self.pin, BASE_FREQ)

    # move to initial POS
    print "Initialise servo at pos", self.pos
    self.servo.start(pulse_length(self.pos))
    time.sleep(T_MAX)
    self.servo.stop()
    time.sleep(1)

  def __del__(self):
    GPIO.cleanup()

  def pulse_length(angle):
    # return pulse length to reach requested angle
    increment = (MAX_POS - MIN_POS) / ANGLE_RANGE
    pl = MIN_POS + (increment * angle)
    print "Pulse length is", pl
    return pl

  def duration(angle):
    # calculate signal duration from current and final position
    diff = abs(self.pos - angle)
    d = T_PER_60/60.0 * diff
    print "Movement duration is", d
    self.pos = angle
    return d

  def move(angle):
    # move 'servo' to 'angle'
    print "Move servo to", angle
    self.servo.start(pulse_length(angle))
    time.sleep(duration(angle))
    self.servo.stop()
    time.sleep(0.5)

  def open():
    # open servo
    print "Open servo"
    move(OPEN_POS)

  def close():
    # close servo
    print "Close servo"
    move(CLOSE_POS)

if __name__ == "__main__":
  # testing
  servo = SMServo(7, 90)
  servo.open()
  servo.close()


from RPIO import PWM
import time
import os

class SMServo:

  # the servo is a 'TowerPro SG90' or similar
  # http://www.servodatabase.com/servo/towerpro/sg90
  # with a pulse width of 500-2400 micro-seconds
  # at an PWM base frequency of 50Hz / period of 20ms

  ANGLE_RANGE = 180 # tested, not for sure
  BASE_FREQ = 50    # user setting
  BASE_PERIOD = 1000.0 * 1/BASE_FREQ
  MIN_PULSE_WIDTH = 500
  MAX_PULSE_WIDTH = 2400 
  NEUTRAL_WIDTH = 0.5 * (MAX_PULSE_WIDTH + MIN_PULSE_WIDTH)
  OPEN_ANGLE = 180
  CLOSE_ANGLE = 0
  
  T_PER_60 = 0.17 # tested, not for sure
  T_MAX = ANGLE_RANGE/60.0 * T_PER_60

  def __init__(self, pin, init_pos):
    # GPIO PWN pin number
    self.pin = pin
    # log current position as hardware feedback is not possible
    # thus, an initialisation value is necessary
    self.pos = init_pos

    # initialise RPIO servo instance
    self.servo = PWM.Servo()

    # move to initial POS
    self.servo.set_servo(self.pin, pulse_length(self.pos))
    time.sleep(T_MAX)
    self.servo.stop_servo(self.pin)
    time.sleep(1)

  def __del__(self):
    PWM.cleanup()

  def pulse_length(angle):
    # return pulse length to reach requested angle
    increment = (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / ANGLE_RANGE
    pl = MIN_PULSE_WIDTH + (increment * angle)
    return pl

  def duration(angle):
    # calculate signal duration from current and final position
    diff = abs(self.pos - angle)
    d = T_PER_60/60.0 * diff
    self.pos = angle
    return d

  def move(angle):
    # move 'servo' to 'angle'
    #print "Move servo to", angle
    self.servo.set_servo(self.pin, pulse_length(angle))
    time.sleep(duration(angle))
    self.servo.stop_servo(self.pin)
    time.sleep(1)

  def open():
    # open servo
    print "Open servo"
    move(OPEN_ANGLE)

  def close():
    # close servo
    print "Close servo"
    move(CLOSE_ANGLE)

if __name__ == "__main__":
  # testing
  servo = SMServo(18, 90)
  servo.open()
  servo.close()


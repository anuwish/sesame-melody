import time
import os

class Servo:
  # create mockup to develop w/o need for an RasPi
  mockup = True
  try:
    from RPIO import PWM
    mockup = False
  except:
    pass

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

    if not Servo.mockup:
      # initialise RPIO servo instance
      self.servo = Servo.PWM.Servo()

      # move to initial POS
      self.servo.set_servo(self.pin, self.pulse_length(self.pos))
      time.sleep(Servo.T_MAX)
      self.servo.stop_servo(self.pin)
      time.sleep(1)
    else:
      print 'smgpio.mech.mockup', '__init__(self, pin, init_pos)'

  def __del__(self):
    if not Servo.mockup:
      Servo.PWM.cleanup()
    else:
      print 'smgpio.mech.mockup', '__del__(self)'

  def pulse_length(self, angle):
    if not Servo.mockup:
      # return pulse length to reach requested angle
      increment = (Servo.MAX_PULSE_WIDTH - Servo.MIN_PULSE_WIDTH) / Servo.ANGLE_RANGE
      pl = Servo.MIN_PULSE_WIDTH + (increment * angle)
      return pl
    else:
      print 'smgpio.mech.mockup', 'pulse_length(self, angle)'   

  def duration(self, angle):
    if not Servo.mockup:
      # calculate signal duration from current and final position
      diff = abs(self.pos - angle)
      d = Servo.T_PER_60/60.0 * diff
      self.pos = angle
      return d
    else:
      print 'smgpio.mech.mockup', 'duration(self, angle)'   

  def move(self, angle):
    if not Servo.mockup:
      # move 'servo' to 'angle'
      #print "Move servo to", angle
      self.servo.set_servo(self.pin, self.pulse_length(angle))
      time.sleep(self.duration(angle))
      self.servo.stop_servo(self.pin)
      time.sleep(1)
    else:
      print 'smgpio.mech.mockup', 'move(self, angle)'   

  def open(self):
    if not Servo.mockup:
      # open servo
      print "Open servo"
      self.move(Servo.OPEN_ANGLE)
    else:
      print 'smgpio.mech.mockup', 'open(self)'   

  def close(self):
    if not Servo.mockup:
      # close servo
      print "Close servo"
      self.move(Servo.CLOSE_ANGLE)
    else:
      print 'smgpio.mech.mockup', 'close(self)'   

if __name__ == "__main__":
  # testing
  servo = Servo(18, 90)
  servo.open()
  servo.close()


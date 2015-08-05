from RPIO import PWM
import time
import os

# output GPIO for the PWM signal 
NGPIO = 18

# the servo is a 'TowerPro SG90' or similar
# http://www.servodatabase.com/servo/towerpro/sg90
# with a pulse width of 500-2400 micro-seconds
# at an PWM base frequency of 50Hz and a period of 20ms
ANGLE_RANGE = 180 # tested, not for sure
BASE_FREQ = 50    # user setting
BASE_PERIOD = 1000.0 * 1/BASE_FREQ
MIN_PULSE_WIDTH = 500
MAX_PULSE_WIDTH = 2400 
NEUTRAL_WIDTH = 0.5 * (MAX_PULSE_WIDTH + MIN_PULSE_WIDTH)

T_PER_60 = 0.17 # tested, not for sure
T_MAX = ANGLE_RANGE/60.0 * T_PER_60

# log current position as hardware feedback is not possible
# thus, an initialisation value is necessary, took center position
POS = 0.5 * ANGLE_RANGE

#print "angle range", ANGLE_RANGE, "base freq", BASE_FREQ, "base period", BASE_PERIOD, "min/max pulse width", MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, "min/max pos", "neutral width", NEUTRAL_WIDTH, "t per 60", T_PER_60, "initial pos", POS

def set_POS(angle):
  global POS
  POS = angle
  print "POS set to", POS

def pulse_length(angle):
  # return pulse length to reach requested angle
  increment = (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / ANGLE_RANGE
  pl = MIN_PULSE_WIDTH + (increment * angle)
  #print "Pulse length is", pl
  return pl

def duration(angle):
  # calculate signal duration from current and final position
  diff = abs(POS - angle)
  d = T_PER_60/60.0 * diff
  #print "Duration is", d
  set_POS(angle)
  return d

def init(servo):
  # initialise servo, move to inital POS
  print "Initialise servo at pos", POS
  servo.set_servo(NGPIO, pulse_length(POS))
  time.sleep(T_MAX)
  servo.stop_servo(NGPIO)
  time.sleep(1)

def move(servo, angle):
  # move 'servo' to 'angle'
  #print "Move servo to", angle
  servo.set_servo(NGPIO, pulse_length(angle))
  time.sleep(duration(angle))
  servo.stop_servo(NGPIO)
  time.sleep(1)


def main():
  servo = PWM.Servo()
  time.sleep(0.2)
  
  init(servo)

  move(servo, 0) 
  move(servo, 180)
  move(servo, 0)

  PWM.cleanup()

main()

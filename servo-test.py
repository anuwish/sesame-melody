import RPi.GPIO as GPIO
import time
import os

# output pin for the PWM signal 
PIN = 7

# the servo is a 'TowerPro SG90' or similar
# http://www.servodatabase.com/servo/towerpro/sg90
# with a pulse width of 500-2400 micro-seconds
# at an PWM base frequency of 50Hz, a period of 20ms
ANGLE_RANGE = 180 # tested, not for sure
BASE_FREQ = 50    # user setting
BASE_PERIOD = 1000.0 * 1/BASE_FREQ
MIN_PULSE_WIDTH = 0.5
MAX_PULSE_WIDTH = 2.4 
MIN_POS = 100.0 * MIN_PULSE_WIDTH/BASE_PERIOD
MAX_POS = 100.0 * MAX_PULSE_WIDTH/BASE_PERIOD
NEUTRAL_POS = 0.5 * (MAX_POS + MIN_POS)

T_PER_60 = 0.17 # tested, not for sure
T_MAX = ANGLE_RANGE/60.0 * T_PER_60

# log current position as hardware feedback is not possible
# thus, an initialisation value is necessary, took center position
POS = 0.5 * ANGLE_RANGE

print "Config:"
print "angle range", ANGLE_RANGE, "base freq", BASE_FREQ, "base period", BASE_PERIOD, "min/max pulse width", MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, "min/max pos", MIN_POS, MAX_POS, "neutral pos", NEUTRAL_POS, "t per 60", T_PER_60, "initial pos", POS

def set_POS(angle):
  global POS
  POS = angle
  print "POS set to", POS

def pulse_length(angle):
  # return pulse length to reach requested angle
  increment = (MAX_POS - MIN_POS) / ANGLE_RANGE
  pl = MIN_POS + (increment * angle)
  print "Pulse length is", pl
  return pl

def duration(angle):
  # calculate signal duration from current and final position
  diff = abs(POS - angle)
  d = T_PER_60/60.0 * diff
  print "Duration is", d
  set_POS(angle)
  return d

def init(servo):
  # initialise servo, move to inital POS
  print "Initialise servo at pos", POS
  servo.start(pulse_length(POS))
  time.sleep(T_MAX)
  servo.stop()
  time.sleep(1)

def move(servo, angle):
  # move 'servo' to 'angle'
  print "Move servo to", angle
  servo.start(pulse_length(angle))
  time.sleep(duration(angle))
  #time.sleep(T_MAX)
  servo.stop()
  time.sleep(0.5)


def main():
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN, GPIO.OUT)

  servo = GPIO.PWM(PIN, BASE_FREQ)
  
  # manual
  servo.start(pulse_length(180))
  time.sleep(T_MAX)
  servo.stop()
  servo.start(pulse_length(0))
  time.sleep(T_MAX)
  servo.stop()
  set_POS(0)
  
  # automated
  move(servo,180)
  move(servo,0)
  #init(servo)
  #time.sleep(2)
  
  GPIO.cleanup()

main()

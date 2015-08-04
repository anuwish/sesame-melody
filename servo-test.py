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

# log current position as hardware feedback is not possible
# thus, an initialisation value is necessary, took center position
POS = 0.5 * ANGLE_RANGE

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
  print "Initialise servo"
  servo.start(pulse_length(POS))
  time.sleep(ANGLE_RANGE/60.0 * T_PER_60)
  servo.stop()
  time.sleep(1)

def move(servo, angle):
  # move 'servo' to 'angle'
  servo.start(pulse_length(angle))
  time.sleep(duration(angle))
  servo.stop()


# define open and close states
def open(servo):
  print "Move servo to open position"
  move(servo, 180)

def close(servo):
  print "Move servo to close position"
  move(servo, 0)


def main():
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN, GPIO.OUT)

  servo = GPIO.PWM(PIN, BASE_FREQ)
  init(servo)
  time.sleep(2)
  
  #neutral(servo)
  open(servo)
  close(servo)
  #open(servo)

  GPIO.cleanup()

main()

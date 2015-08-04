import RPi.GPIO as GPIO
import time
import os

PIN = 7


def neutral(s):
  s.start(7.5)
  time.sleep(1)
  s.stop()

def open(s):
  s.start(10)
  time.sleep(0.5)
  s.stop()

def close(s):
  s.start(5)
  time.sleep(0.5)
  s.stop()

def main():
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN, GPIO.OUT)

  servo = GPIO.PWM(PIN, 50)

  close(servo)
  open(servo)

  GPIO.cleanup()

main()

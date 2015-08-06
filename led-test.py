import RPi.GPIO as GPIO
import time
import os

# output pin for the LED signal 
PIN_RED = 15
PIN_GREEN = 16
PINS = [PIN_RED, PIN_GREEN]

def red():
  GPIO.output(PINS, (GPIO.HIGH, GPIO.LOW))

def green():
  GPIO.output(PINS, (GPIO.LOW, GPIO.HIGH))

def yellow():
  GPIO.output(PINS, (GPIO.HIGH, GPIO.HIGH))

def off():
  GPIO.output(PINS, (GPIO.LOW, GPIO.LOW))

def main():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PINS, GPIO.OUT)

  for i in range(10):
    red()
    time.sleep(0.5)
    off()
    time.sleep(0.2)
    green()
    time.sleep(0.5)
    off()
    time.sleep(0.2)
    yellow()
    time.sleep(0.5)
    off()
    time.sleep(0.2)

  GPIO.cleanup()

main()

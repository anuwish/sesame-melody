import RPi.GPIO as GPIO
import time
import os

# Pin 7 als Ausgang deklarieren
#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

servo = GPIO.PWM(7, 50)
servo.start(10)
time.sleep(0.1)
servo.stop()

GPIO.cleanup()

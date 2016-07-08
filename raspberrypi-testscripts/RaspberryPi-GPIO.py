#! /usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output(16, True)
GPIO.output(18, True)
time.sleep(5)
GPIO.output(16, False)
GPIO.output(18, False)
GPIO.cleanup()

#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	input_state = GPIO.input(18)
	if input_state == False:
                os.system('/home/pi/lm.py')
		time.sleep(0.5)
                os.system('/home/pi/lm2.py')
		time.sleep(0.5)

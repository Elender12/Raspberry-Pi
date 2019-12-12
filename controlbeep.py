"""/usr/bin/python
$      Filename      :controlbeep.py
$      Description   :If KEY_4 is pressed,this script will be executed
$      Author        :alan
$      Website       :www.osoyoo.com
$      Update        :2017/07/07
$      
$      
"""
import RPi.GPIO as GPIO

PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN, GPIO.IN)
GPIO.setup(PIN, GPIO.OUT)

if GPIO.input(PIN) == 0:
     GPIO.output(PIN, GPIO.HIGH)
     print('close buzzer\n')
else:
     GPIO.output(PIN, GPIO.LOW)
     print('open buzzer\n')


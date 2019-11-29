#!/usr/bin/python
###########################################################################
#Filename      :button_led.py
#Description   :button control led
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/06/27
############################################################################

import RPi.GPIO as GPIO
import time

#set BCM_GPIO 17(GPIO0) as button pin
ButtonPin = 17
#set BCM_GPIO 18(GPIO1) as LED pin
LedPin = 18

#set led status to True(OFF)
led_status = True

#print message at the begining ---custom function
def print_message():
    print ('|**********************************|')
    print ('|           Button control LED     |')
    print ('|  ------------------------------  |')
    print ('|        LED Connect to GPIO1      |')
    print ('|       Button Connect to GPIO0    |')
    print ('|  ------------------------------  |')
    print ('|                                  |')
    print ('|                            OSOYOO|')
    print ('|**********************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    pass

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set all LedPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(LedPin,GPIO.OUT,initial=GPIO.HIGH)
    #set ButtonPin's mode to input,and pull up to high(3.3v)
    GPIO.setup(ButtonPin,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    #set up a falling detect on ButtonPin,and callback function to ButtonLed
    GPIO.add_event_detect(ButtonPin,GPIO.FALLING,callback = ButtonLed)
    pass

#define a callback function for button callback
def ButtonLed(ev=None):
    global led_status
    # Switch led status(on-->off; off-->on)
    led_status = not led_status
    GPIO.output(LedPin, led_status)
    if led_status:
        print('|*************|')
        print('|  LED OFF... |')
        print('|*************|')
        print('\n')
    else:
        print('|*************|')
        print('|  ...LED ON  |')
        print('|*************|')
        print('\n')

# Define a main function for main process
def main():
    # Print messages
    print_message()
    while True:
        # Don't do anything.
        time.sleep(1)

# Define a destroy function for clean up everything after
# the script finished 
def destroy():
    # Turn off LED
    GPIO.output(LedPin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()
    pass

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program 
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()


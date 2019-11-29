#!/usr/bin/python
###########################################################################
#Filename      :flow_led.py
#Description   :make a flow led
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/06/26
############################################################################

import RPi.GPIO as GPIO
import time

# set 8 pins for 8 leds.
LedPins = [17,18,27,22,23,24,25,26]

#print message at the begining ---custom function
def print_message():
    print ('******************************')
    print ('|            flow leds       |')
    print ('|     ---------------------  |')
    print ('|   LED_R1 connect to GPIO0  |')
    print ('|   LED_R2 connect to GPIO1  |')
    print ('|   LED_G1 connect to GPIO2  |')
    print ('|   LED_G2 connect to GPIO3  |')
    print ('|   LED_Y1 connect to GPIO4  |')
    print ('|   LED_Y2 connect to GPIO5  |')
    print ('|   LED_W1 connect to GPIO6  |')
    print ('|   LED_W2 connect to GPIO7  |')
    print ('|        ----------------    |')
    print ('|                            |')
    print ('|              nope    OSOYOO|')
    print ('****************************\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    


#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set all LedPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(LedPins,GPIO.OUT,initial=GPIO.HIGH)


#main function
def main():
    #print info
    print_message()
    while True:
        #turn LED on from left to right
        print("***********************")
        print("       ----->>         ")
        print("  From Left To Right!  ")
        print("***********************")
        for pin in LedPins:
            GPIO.output(pin,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(pin,GPIO.HIGH)
            pass

        #turn LED on from right to left
        print("***********************")
        print("       <<-----         ")
        print("  From Right To Left!  ")
        print("***********************")
        for pin in reversed(LedPins):
            GPIO.output(pin,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(pin,GPIO.HIGH)

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off all LEDs
    GPIO.output(LedPins,GPIO.HIGH)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()

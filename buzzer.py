
#!/usr/bin/python

###########################################################################
#Filename      :buzzer.py
#Description   :make buzzer beep
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/06/27
############################################################################

import RPi.GPIO as GPIO
import time

# Set #18 as buzzer pin
BuzzerPin = 18

def print_message():
    print ("|**************************************|")
    print ("|                 Beep                 |")
    print ("|    ------------------------------    |")
    print ("|        Buzzer connect to GPIO1       |")
    print ("|                                      |")
    print ("|            Make Buzzer beep          |")
    print ("|                                      |")
    print ("|                                OSOYOO|")
    print ("|**************************************|\n")
    print 'Program is running...'
    print ('\n')
    print 'Please press Ctrl+C to end the program...'

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set BuzzerPin's mode to output, 
    # and initial level to High(3.3v)
    GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.HIGH)

def main():
    print_message()
    while True:
    	GPIO.output(BuzzerPin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(BuzzerPin, GPIO.HIGH)
        time.sleep(1)

def destroy():
    # Turn off buzzer
    GPIO.output(BuzzerPin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()    

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program 
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()

  

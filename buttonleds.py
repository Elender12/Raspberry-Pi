
import RPi.GPIO as GPIO

import time



LEDPINS = [12,25,23,18,4,17,27,22]

buttonPin = 26



def setup():

    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LEDPINS,GPIO.OUT,initial=GPIO.LOW)

    GPIO.setup(buttonPin,GPIO.IN,pull_up_down = GPIO.PUD_UP)

    GPIO.add_event_detect(buttonPin,GPIO.FALLING, callback = buttonLed)

    pass



def buttonLed(ev=None):
    led_status = True
    led_status = not led_status

    if led_status:

        print("apagado.")

    else:

        for pin in LEDPINS:

            GPIO.output(pin,GPIO.HIGH)
	    time.sleep(0.3)
            GPIO.output(pin,GPIO.LOW)
	    time.sleep(0.3)


def destroy():

    for pin in LEDPINS:

            GPIO.output(pin,GPIO.LOW)

            GPIO.cleanup()



try:

    setup()

    buttonLed()

except KeyboardInterrupt:

    destroy()



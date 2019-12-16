import RPi.GPIO as GPIO
import time
import os
import smbus
import random
from gpiozero import LED, Button

#configuracion general
PIN_WHITE= LED(17)
PIN_GREEN= LED(20)
PIN_BUZZER= 21
BUTTON_WHITE= Button(19)
BUTTON_GREEN= Button(26)
led_status = True
PIN_WHITE.toggle()
PIN_GREEN.toggle()




#configuracion pantalla
# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line
# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off
ENABLE = 0b00000100 # Enable bit
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
def lcd_init():
 # Initialise display
 lcd_byte(0x33,LCD_CMD) # 110011 Initialise
 lcd_byte(0x32,LCD_CMD) # 110010 Initialise
 lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
 lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
 lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
 lcd_byte(0x01,LCD_CMD) # 000001 Clear display
 time.sleep(E_DELAY)
def lcd_byte(bits, mode):
 # Send byte to data pins
 # bits = the data
 # mode = 1 for data
 #        0 for command
 bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
 bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
 # High bits
 bus.write_byte(I2C_ADDR, bits_high)
 lcd_toggle_enable(bits_high)
 # Low bits
 bus.write_byte(I2C_ADDR, bits_low)
 lcd_toggle_enable(bits_low)
def lcd_toggle_enable(bits):
 # Toggle enable
 time.sleep(E_DELAY)
 bus.write_byte(I2C_ADDR, (bits | ENABLE))
 time.sleep(E_PULSE)
 bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
 time.sleep(E_DELAY)
def lcd_string(message,line):
 # Send string to display
 message = message.ljust(LCD_WIDTH," ")
 lcd_byte(line, LCD_CMD)
 for i in range(LCD_WIDTH):
   lcd_byte(ord(message[i]),LCD_CHR)


# Main program block
def main():
 # Initialise display
 lcd_init()
 while True:
   # Send some test
   lcd_string("  linea 1",LCD_LINE_1)
   lcd_string("   <3P    ",LCD_LINE_2)
   time.sleep(3) # Send some more text lcd_string("> Tutorial Url:",LCD_LINE_1)
   lcd_string(" pedro mola <3 ",LCD_LINE_1)
   lcd_string("  pedro vuelve a molar",LCD_LINE_2)
   time.sleep(3)
   lcd_string(" siempre molas",LCD_LINE_1)
   lcd_string(" sigues molando",LCD_LINE_2)
   time.sleep(3)

def saludo():
    namePlayerWhite= input("Introduzca tu nombre PLAYERWHITE: ")
    namePlayerGreen= input("Introduzca tu nombre PLAYERGREEN: ")
    if namePlayerWhite=="" or namePlayerGreen=="":
        lcd_init()
        lcd_string("Empty field",LCD_LINE_1)
        lcd_string("Try again",LCD_LINE_2)
        time.sleep(3)
        saludo()
    else:
        lcd_init()
   # Send some test
        lcd_string("Welcome",LCD_LINE_1)
        lcd_string("Players:",LCD_LINE_2)
        time.sleep(3) # Send some more text lcd_string("> Tutorial Url:",LCD_LINE_1)
        lcd_string(namePlayerWhite,LCD_LINE_1)
        lcd_string(namePlayerGreen,LCD_LINE_2)
        time.sleep(3)
    return namePlayerWhite,namePlayerGreen
def game(white, green):
    #GPIO.setup(BUTTON_WHITE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(BUTTON_GREEN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        #GPIO.add_event_detect(BUTTON_WHITE,GPIO.FALLING,callback= mensajeTest)
        #GPIO.add_event_detect(BUTTON_GREEN,GPIO.FALLING,callback= otroTest)
    #DEFINIR CONTADORES
    white_counter = 0
    green_counter = 0
    #atentos()
    while white_counter<3 and green_counter<3:
        atentos()

        if BUTTON_WHITE.is_pressed:
           white_counter= white_counter+ 1
           PIN_WHITE.toggle()
           time.sleep(1)
           PIN_WHITE.toggle()

        if BUTTON_GREEN.is_pressed:
           green_counter= green_counter+1
           PIN_GREEN.toggle()
           time.sleep(1)
           PIN_GREEN.toggle()
        #BUTTON_GREEN.is_pressed = PIN_GREEN.on
        #BUTTON_WHITE.when_pressed = otroTest

        #BUTTON_GREEN.when_released = PIN_GREEN.on
        #BUTTON_GREEN.when_released = PIN_GREEN.off
        #time.sleep(3)
        lcd_init()
        lcd_string("White: "+str(white_counter),LCD_LINE_1)
        lcd_string("Green: "+str(green_counter),LCD_LINE_2)
        time.sleep(3)
    #print("contador blanco ",white_counter)
    #print("contador verde ",green_counter)
    #GPIO.cleanup()
    #lcd_init()
    #lcd_string("mehhh",LCD_LINE_1)
    #time.sleep(3)
    if green_counter == 3:
        print("estoy dentro del if: verde ")
        lcd_init()
        lcd_string("Green wins",LCD_LINE_1)
        lcd_string(" xD",LCD_LINE_2)
        time.sleep(3)
    if white_counter == 3:
        print("estoy dentro del if: blanco ")
        #lcd_init()
        lcd_string("White wins",LCD_LINE_1)
        lcd_string("chaval",LCD_LINE_2)
        time.sleep(3)
        #print("contador blanco ",white_counter)

#def boton():


def atentos():
    lcd_init()
    lcd_string(" Estad",LCD_LINE_1)
    lcd_string("     atentos...",LCD_LINE_2)
    sonidito()

def sonidito():
    #en timeRND tiempo activara el sonido
    timeRND = random.randint(5,10)
    #se activa el sonido
    time.sleep(timeRND)
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    #time.sleep(0.3)

#pendiente editar
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(PIN_WHITE, GPIO.OUT, initial=GPIO.HIGH)
    #GPIO.setup(PIN_GREEN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.HIGH)
    #GPIO.setup(BUTTON_WHITE, GPIO.FALLING, callback= ButtonLed )
    #GPIO.setup(BUTTON_WHITE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(BUTTON_GREEN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.add_event_detect(BUTTON_WHITE,GPIO.FALLING,callback= mensajeTest)
    #GPIO.add_event_detect(BUTTON_GREEN,GPIO.RISING,callback= otroTest)
    #GPIO.setup()
def mensajeTest():
    print("Boton blanco")
def otroTest():
    print("Boton verde")

setup()
try:
    name1, name2 =saludo()
    game(name1, name2)
   #main()
except KeyboardInterrupt:
   pass
finally:
   lcd_byte(0x01, LCD_CMD)
#!/usr/bin/python
###########################################################################
#Filename      :voltmeter.py
#Description   :make a voltmeter.
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/06/04
############################################################################
import time
import os
import RPi.GPIO as GPIO
import smbus

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

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
analogChannel = 0

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
#setup function for some setup---custom function
def setup():
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    pass

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

    
#print message at the begining ---custom function
def print_message():
    print ('|**********************************|')
    print ('|              Voltmeter           |')
    print ('|    -------------------------     |')
    print ('|    | ADC |           | Pi  |     |')
    print ('|    |-----|-----------|-----|     |')
    print ('|    | CS  | connect to| CE0 |     |')
    print ('|    | Din | connect to| MOSI|     |')
    print ('|    | Dout| connect to| MISO|     |')
    print ('|    | CLK | connect to| SCLK|     |')
    print ('|    | CH0 | connect to| 3.3V|     |')
    print ('|    | CH1 | connect to| GND |     |')
    print ('|    -------------------------     |')
    print ('|   Potentiometer connect to CH0   |')
    print ('|                            OSOYOO|')
    print ('|**********************************|\n')
    
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

#main function
def main():
    #print info
    print_message()
    # Initialise display
    lcd_init()
    #clear screen
    lcd_byte(0x01, LCD_CMD)
    while True:
        adc = readadc(analogChannel, SPICLK, SPIMOSI, SPIMISO, SPICS)
        voltage = round((adc/1024.*3.3),2)
        voltage = str(voltage)     #float change to string
        lcd_string("por que no vas?        <",LCD_LINE_1)
        lcd_string(voltage,LCD_LINE_2)
        time.sleep(1.5)
        
#define a destroy function for clean up everything after the script finished
def destroy():
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
        pass
    #clear screen
    finally:
        lcd_byte(0x01, LCD_CMD)



from lirc import RawConnection
from gpiozero import LED, Button
import RPi.GPIO as GPIO
import smbus
import time
import random
from calculadora_loca import mainCalc
from hermano_sinonimo import mainSynonym
#testMain= calculadora_loca.mainCalc

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line
FEED_BUTTON = Button(26)
GREEN_PIN = LED(23)
YELLOW_PIN = LED(18)
RED_PIN = LED(25)

GREEN_PIN.toggle()
YELLOW_PIN.toggle()
RED_PIN.toggle()

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
    #lcd_byte(0x01, LCD_CMD)
    '''lcd_byte(64,LCD_CMD)
    lcd_byte(16,LCD_CHR)
    lcd_byte(24,LCD_CHR)
    lcd_byte(28,LCD_CHR)
    lcd_byte(30,LCD_CHR)
    lcd_byte(28,LCD_CHR)
    lcd_byte(24,LCD_CHR)
    lcd_byte(16,LCD_CHR)
    lcd_byte(0,LCD_CHR)
    lcd_byte( LCD_LINE_1, LCD_CMD)
    lcd_byte(0,LCD_CHR)'''

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


def ProcessIRRemote():

    #get IR command
    #keypress format = (hexcode, repeat_num, command_key, remote_id)
    try:
        keypress = conn.readline(.0001)
    except:
        keypress=""

    if (keypress !="" and keypress != None):

        data = keypress.split()
        sequence = data[1]
        command = data[2]

        #ignore command repeats
        if (sequence != "00"):
           return

        return(command)



#DORMIR= "KEY_0"
#COMER= "KEY_1"
#JUGAR= "KEY_2"
command=""

#devuelve lo que el usuario responde
def remoteResult():
    respuestaUsuario=""
    while True:
        command = ProcessIRRemote()
        #print(command)
        if(command == "KEY_0"):
            #el manda a Naxito a dormir
            respuestaUsuario = "DORMIR"
            break
        if(command == "KEY_1"):
            #el usuario manda a Naxito a comer
            respuestaUsuario= "COMER"
            break
        if(command == "KEY_2"):
            #el usuario manda a Naxito a jugar
            respuestaUsuario= "JUGAR"
            break
        if(command == "KEY_3"):
            #el usuario manda a Naxito a jugar
            respuestaUsuario= "SALIR"
            break

    return respuestaUsuario


#******************CUIDADO CON LO DE ABAJO******************
conn = RawConnection()
def main():
    contComer=0
    contDormir=0
    contJugar=0

    lcd_init()
    lcd_string("  (^ . ^)/ ",LCD_LINE_1)
    #lcd_string(126,LCD_LINE_1)
    lcd_string("> I'm Naxito! <3",LCD_LINE_2)
    time.sleep(3)
    naxitosLife(contComer,contDormir,contJugar)

def naxitosLife(contComer,contDormir,contJugar):
    lcd_string(" d(^ . ^)b ",LCD_LINE_1)
    lcd_string("hazme casiito",LCD_LINE_2)
    command = remoteResult();


    print("valor de comando en naxito life",command)
#para dormir
    if  command == "DORMIR":
        command=""
        YELLOW_PIN.toggle()
        if contComer == 0 and contJugar>=1:
            #aqui duerme
            contDormir+=1
            contJugar-=1
            #mostrar LCD con ZzzZzZzZ
            lcd_string("ZzZzZzZzZ",LCD_LINE_1)
            lcd_string("*sleeping...*",LCD_LINE_2)
            time.sleep(3)
            command=""
        elif contComer>0 and contJugar<1:
            #mostrar LCD "Pero yo quiero jugar..." y debe volver al menú
            lcd_string("But I want to...",LCD_LINE_1)
            lcd_string("      PLAY!",LCD_LINE_2)
            time.sleep(3)
        elif contComer==0 and contJugar==0:
            lcd_string("FEED OR PLAY",LCD_LINE_1)
            lcd_string(" with me...>:(",LCD_LINE_2)
            time.sleep(3)
        YELLOW_PIN.toggle()

        naxitosLife(contComer,contDormir,contJugar)
    #para comer
    if command == "COMER":
        RED_PIN.toggle()
        lcd_string(" (^ . ^)",LCD_LINE_1)
        lcd_string("Gimme food",LCD_LINE_2)
        #cuando le da al botón:
        #print(contComer)
        command=""
        while True:
            if FEED_BUTTON.is_pressed:

                lcd_string(" *(^ o ^)*",LCD_LINE_1)
                lcd_string("NOM NOM NOM...",LCD_LINE_2)
                time.sleep(0.7)
                lcd_string(" *(^ _ ^)*",LCD_LINE_1)
                time.sleep(0.7)
                lcd_string(" *(^ o ^)*",LCD_LINE_1)
                time.sleep(0.7)
                lcd_string(" *(^ _ ^)*",LCD_LINE_1)
                time.sleep(2)
                contComer+=1
                if contComer < 3:
                    break
            #imprimir msj "(❤___❤)"
                if contComer==3:
                    lcd_string("  (^ 3 ^)",LCD_LINE_1)
                    lcd_string("I'm full...",LCD_LINE_2)
                    time.sleep(2)
                    break
                if contComer==4:
                    lcd_string("  (T  n  T)",LCD_LINE_1)
                    lcd_string("I'm fat... stop",LCD_LINE_2)
                    time.sleep(2)
                    break
                if contComer==5:
                    lcd_string("  (X ___ x)",LCD_LINE_1)
                    lcd_string("    -D E A D-",LCD_LINE_2)
                    time.sleep(2)
                    exit()
                    break

        RED_PIN.toggle()
        print(contComer)
        naxitosLife(contComer,contDormir,contJugar)
    if command == "JUGAR" and contComer>=1:
        GREEN_PIN.toggle()
        lcd_string("  (^ . ^)",LCD_LINE_1)
        lcd_string("LET'S PLAY",LCD_LINE_2)
        time.sleep(0.7)
        lcd_string("  (* o *)",LCD_LINE_1)
        lcd_string("LET'S PLAY...",LCD_LINE_2)
        time.sleep(1.5)
        lcd_string("  (o - o) ?",LCD_LINE_1)
        lcd_string("    a GAME!",LCD_LINE_2)
        time.sleep(1.5)
        command=""
        #choice = random.randint(1,2)
        choice=1
        print(choice)
        while True:
            if choice == 1:
                mainCalc()
                contJugar+=1
                contComer-=1
                break
            else:
                mainSynonym()
                contJugar+=1
                contComer-=1
                break

        print(contComer,"el valor de contador comida")
        GREEN_PIN.toggle()
        command=""
        naxitosLife(contComer,contDormir,contJugar)
    elif command == "JUGAR" and contComer<1:
        lcd_string("  ('- _ -) ",LCD_LINE_1)
        lcd_string(" I am HUNGRY!",LCD_LINE_2)
        time.sleep(2)
        command=""
        naxitosLife(contComer,contDormir,contJugar)
    if command == "SALIR":
        lcd_string("  (n _ n) ",LCD_LINE_1)
        lcd_string(" Goodbye!!",LCD_LINE_2)
        time.sleep(2)
        command=""

#*************BLOQUE FINAL*************
try:
    main()
except KeyboardInterrupt:
    print("// Control C interrupt")
    pass
finally:
    lcd_byte(0x01, LCD_CMD)
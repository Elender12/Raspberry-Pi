from lirc import RawConnection
import RPi.GPIO as GPIO
import smbus
import time
import random

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change t       his address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command1

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

connMath = RawConnection()
def ProcessIRRemote1():

    #get IR command1
    #keypress format = (hexcode, repeat_num, command1_key, remote_id)
    try:
        #keypress=""
        keypress = connMath.readline(.0001)
    except:
        keypress=""

    if (keypress !="" and keypress != None):

        data = keypress.split()
        sequence = data[1]
        command1 = data[2]

        #ignore command1 repeats
        if (sequence != "00"):
           return

        return(command1)

def sumar():
    num1 = random.randint(1,99)
    num2 = random.randint(1,99)
    #lcd_string(str(num1)+ "+"+str(num2),LCD_LINE_1)
    operacion = str(num1)+" + "+str(num2)
    res = num1+num2
    #capturar resultado del usuario
    return res, operacion

def restar():
    num1 = random.randint(1,99)
    num2 = random.randint(1,99)
    while num1<num2:
        num1 = random.randint(1,99)
    operacion = str(num1)+" - "+str(num2)
    res = num1-num2
    #capturar resultado del usuario
    return res, operacion

def multiplicar():
    num1 = random.randint(1,20)
    num2 = random.randint(1,20)
    res = num1*num2
    #capturar resultado del usuario
    operacion = str(num1)+" * "+str(num2)
    return res, operacion

command1 =""
def remoteResult1(operacion):
    lcd_init()
    #define Global

    var=""
    userRes=0
    #print(var,"el valor de variable!")
    #print(command1,"el valor de command1")

    #print("dentro de remoteResult")
    command1 = ProcessIRRemote1()
    command1=""
    while True:
        lcd_string(operacion+" = ?",LCD_LINE_1)
        lcd_string(var,LCD_LINE_2)

        command1 = ProcessIRRemote1()
        #var=""
        #print(command1)
        print(var,"el valor de variable dentro del while true")
        print(command1,"el valor de command1 dentro del while true")

        if(command1 == "KEY_0"):
            var+="0"
        if(command1 == "KEY_1"):
            var+="1"
        if(command1 == "KEY_2"):
            var+="2"
        if(command1 == "KEY_3"):
            var+="3"
        if(command1 == "KEY_4"):
            var+="4"
        if(command1 == "KEY_5"):
            var+="5"
        if(command1 == "KEY_6"):
            var+="6"
        if(command1 == "KEY_7"):
            var+="7"
        if(command1 == "KEY_8"):
            var+="8"
        if(command1 == "KEY_9"):
            var+="9"
        if(command1 == "KEY_PREVIOUS"):
            var=""
        if(command1 == "KEY_EQUAL"):
            if var == "":
                var = 0
            userRes = int(var)
            lcd_byte(0x01, LCD_CMD)
            break
    command1 = ProcessIRRemote1()
    command1=""
    print(userRes, "user res tiene el valor")
    return userRes

def mainCalc():
    print("Running...")
    print("Look at the LCD!")
    lcd_byte(0x01, LCD_CMD)
    lcd_string("  -First game- ",LCD_LINE_1)
    lcd_string("> Do the math!:)",LCD_LINE_2)
    time.sleep(5)
    cont=0
    Vcont=0
    while cont<5:
        cont+=1
        choice = random.randint(1,3)
        #choice= 1
        if choice==1:
            res,operacion = sumar()
            userRes = remoteResult1(operacion)
            if res==userRes:
                lcd_string("  -CORRECT-",LCD_LINE_1)
                Vcont+=1
                time.sleep(3)
            else:
                lcd_string(" -INCORRECT-",LCD_LINE_1)
                time.sleep(3)
        elif choice==2:
            res, operacion = restar()
            userRes = remoteResult1(operacion)
            if res==userRes:
                lcd_string("  -CORRECT-",LCD_LINE_1)
                Vcont+=1
                time.sleep(3)
            else:
                lcd_string(" -INCORRECT-",LCD_LINE_1)
                time.sleep(3)
            #print(res)
        elif choice==3:
            res, operacion = multiplicar()
            userRes = remoteResult1(operacion)
            if res==userRes:
                lcd_string("  -CORRECT-",LCD_LINE_1)
                Vcont+=1
                time.sleep(3)
            else:
                lcd_string(" -INCORRECT-",LCD_LINE_1)
                time.sleep(3)
            #print(res)
        else:
            lcd_string(" -E R R O R-",LCD_LINE_1)
            time.sleep(3)
    lcd_string("Correct answers",LCD_LINE_1)
    lcd_string("> "+str(Vcont),LCD_LINE_2)
    time.sleep(3)

'''try:
    mainCalc()
except KeyboardInterrupt:
    print("// Control C interrupt")
    pass
finally:
    lcd_string("Time to go back",LCD_LINE_1)
    lcd_string("  with Naxito!",LCD_LINE_2)
    time.sleep(3)
    lcd_byte(0x01, LCD_CMD)'''
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

#muestra una de las palabras en la linea 1
sinonimos1= ["vasto","calumnia","hablador","perfidia","hosco","ofuscar","disyuntiva","tupido","dorso","pusilanime"]
#muestra una de las palabras en la linea 2
sinonimos2=["amplio","falsedad","locuaz","traicion","aspero","perturbar","dilema","claro","anverso","bizarro"]

#muestro las claves
#print(diccionarioVerificacion.keys())
#print(sinonimos1[0],sinonimos2[2])

#******************CUIDADO CON LO DE ABAJO******************
conn = RawConnection()
def verificarRespuesta(palabra1, palabra2):
    #diccionario de verificacion
    diccionarioVerificacion= {
        "vasto": "amplio",
        "calumnia": "falsedad",
        "hablador": "locuaz",
        "perfidia": "traicion",
        "hosco": "aspero",
        "ofuscar": "perturbar",
        "disyuntiva":"dilema",
        "tupido": "claro"
}
    valor = diccionarioVerificacion.get(palabra1)

    if valor == palabra2:
        return True
        #print("son sinonimos")
    else:
        return False
        #print("nope")

def mainSynonym():
    print("Running...❤")
    print("Look at the LCD!")
    lcd_init()
    lcd_string("  -Second game- ",LCD_LINE_1)
    lcd_string("> Synonym?:/",LCD_LINE_2)
    time.sleep(5)
    cont=0
    Vcont=0
    #print(sinonimos1[aleatorio1],sinonimos2[aleatorio2])
    #recoger la respuesta
    #KEY_VOLUMEDOWN  negativo - no son sinonimos
    #KEY_VOLUMEUP positivo- son sinonimos

    while cont<5:
        aleatorio1= random.randint(0,9)
        aleatorio2= random.randint(0,9)
        lcd_string(sinonimos1[aleatorio1],LCD_LINE_1)
        lcd_string(sinonimos2[aleatorio2],LCD_LINE_2)
        #time.sleep(3)
        cont+=1
        respuesta = verificarRespuesta(sinonimos1[aleatorio1],sinonimos2[aleatorio2])
        respuestaUsuario= remoteResult()
        if respuesta== respuestaUsuario:
            lcd_string("Acertado",LCD_LINE_1)
            lcd_string(":)",LCD_LINE_2)
            time.sleep(3)
            Vcont+=1
        else:
            lcd_string("Nope",LCD_LINE_1)
            lcd_string(":(",LCD_LINE_2)
            time.sleep(3)
#devuelve lo que el usuario responde
def remoteResult():
    command = ProcessIRRemote()
    command=""
    while True:
        command = ProcessIRRemote()
        #print(command)
        if(command == "KEY_VOLUMEDOWN"):
            #el usuario dice que no son sinonimos
            respuestaUsuario= False
            break
        if(command == "KEY_VOLUMEUP"):
            #el usuario dice que son sinonimos
            respuestaUsuario= True
            break

    return respuestaUsuario


#*************BLOQUE FINAL*************
'''try:
    main()
except KeyboardInterrupt:
    print("// Control C interrupt")
    pass
finally:
    lcd_string("Time to go back",LCD_LINE_1)
    lcd_string("  with Naxito!",LCD_LINE_2)
    time.sleep(3)
    lcd_byte(0x01, LCD_CMD)'''
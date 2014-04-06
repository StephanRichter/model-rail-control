import time
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

GPIO.setmode(GPIO.BCM);
GPIO.setwarnings(False);

# Register
SPI_IODIRA     = 0x00
SPI_IODIRB     = 0x01

SPI_POL_A      = 0x02
SPI_POL_B      = 0x03

SPI_CONFIG_A   = 0x0A
SPI_CONFIG_B   = 0x0B

SPI_PULLUP_A   = 0x0C
SPI_PULLUP_B   = 0x0D

SPI_GPIOA      = 0x12
SPI_GPIOB      = 0x13


# Werte
SPI_BASE_ADRESS = 0x40
SPI_SLAVE_WRITE = 0x00
SPI_SLAVE_READ  = 0x01
SPI_HW_ADDR     = 0x08

# MCP23S17-Pins
SCLK = 25 # Serial clock
MOSI = 18 # Master-Out-Slave-In
MISO = 23 # Master-In-Slave-Out
CS   = 24 # Chip-Select

ledPattern = 1

GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)
    
# Pegel vorbereiten
GPIO.output(CS,  GPIO.HIGH);
GPIO.output(SCLK, GPIO.LOW);

def sendValue(value):
    # wert senden
    for i in range(8):
        if (value & 0x80):
            GPIO.output(MOSI, GPIO.HIGH)
        else:
            GPIO.output(MOSI, GPIO.LOW)
        # negative flanke des clocksignals generieren
        GPIO.output(SCLK, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)
        value <<=1 # Bitfolge eine Position nach links schieben
        

def sendSPI(address, register, data):
    opcode = address<<1 | SPI_BASE_ADRESS
    
    GPIO.output(CS, GPIO.LOW)    # CS aktiv (LOW-Aktiv)    
    sendValue(opcode)
    sendValue(register)
    sendValue(data)    
    GPIO.output(CS, GPIO.HIGH) # CS inaktiv

def activateAdressing():
    sendSPI(0, SPI_CONFIG_A, SPI_HW_ADDR)
    sendSPI(0, SPI_CONFIG_B, SPI_HW_ADDR)

def initMCP23S17(addr,portsA,portsB):
    sendSPI(addr, SPI_PULLUP_A, portsA) # Pullups (de)aktivieren    
    sendSPI(addr, SPI_IODIRA, portsA) # In/Out setzen
    sendSPI(addr, SPI_POL_A,portsA) # Logik invertieren
    sendSPI(addr, SPI_PULLUP_B, portsB) # Pullups (de)aktivieren
    sendSPI(addr, SPI_IODIRB, portsB) # In/Out setzen
    sendSPI(addr, SPI_POL_B,portsB) # Logik invertieren
    
def readSPI(address, register):
    opcode = address<<1 | SPI_BASE_ADRESS
    GPIO.output(CS, GPIO.LOW)    # CS aktiv (Low-Aktiv)
    sendValue(opcode|SPI_SLAVE_READ) # opcode senden
    sendValue(register)
        
    # empfangen
    value = 0
    for i in range(8):
        value <<= 1 # 1 position nach links schieben
        if (GPIO.input(MISO)):
            value |= 0x01
        # abfallende flanke generieren
        GPIO.output(SCLK, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)
        
    GPIO.output(CS, GPIO.HIGH)# CS deaktivieren    
    return value
    
if __name__ == '__main__':
    print "running mcp23s17._main_"
    addr=0
    initMCP23S17(addr,0xFF,0x00)
    while True:
        sendSPI(addr, SPI_GPIOB, ledPattern)
        val = readSPI(0, SPI_GPIOA)
        print val
        if (val != 0):
            time.sleep(5)
        time.sleep(0.01)
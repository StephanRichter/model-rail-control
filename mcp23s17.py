








from thread import start_new_thread, allocate_lock
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM);
#GPIO.setwarnings(False);

# MCP23S17 Werte
SPI_SLAVE_ADDR = 0x40
SPI_IOCTRL     = 0x0A
SPI_IODIRA     = 0x00
SPI_IODIRB     = 0x01
SPI_GPIOA      = 0x12
SPI_GPIOB      = 0x13
SPI_PULLUP_A   = 0x0C
SPI_POL_A      = 0x02
SPI_SLAVE_WRITE = 0x00
SPI_SLAVE_READ  = 0x01

# MCP23S17-Pins
SCLK = 18 # Serial clock
MOSI = 24 # Master-Out-Slave-In
MISO = 23 # Master-In-Slave-Out
CS   = 25 # Chip-Select

ledPattern = (0b00001110,\
              0b00011100,\
              0b00111000,\
              0b01110000,\
              0b11100001,\
              0b11000011,\
              0b10000111)

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
        
def sendSPI(opcode, addr, data):
    # CS aktiv (LOW-Aktiv)
    GPIO.output(CS, GPIO.LOW)
    
    sendValue(opcode)
    sendValue(addr)
    sendValue(data)
    
    # CS inaktiv
    GPIO.output(CS, GPIO.HIGH)
    
def readSPI(opcode, addr):
    # CS aktiv (Low-Aktiv)
    GPIO.output(CS, GPIO.LOW)
    
    sendValue(opcode|SPI_SLAVE_READ) # opcode senden
    sendValue(addr)
    
    # empfangen
    value = 0
    for i in range(8):
        value <<= 1 # 1 position nach links schieben
        if (GPIO.input(MISO)):
            value |= 0x01
        # abfallende flanke generieren
        GPIO.output(SCLK, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)
        
    # CS deaktivieren
    GPIO.output(CS, GPIO.HIGH)
    return value

brake_active = False
brkae_lock = allocate_lock()

def brake(time):
    global brake_active
    print "test"
    brake_lock.acquire()
    if (brake_aktive):
        brake_lock.release()
        return
    brake_active = True_
    brake_lock.release()
    print "preparing brake"
    sleep(time)
    print "brake"
    
    
def main():
    # Programmierung der Pins
    GPIO.setup(SCLK, GPIO.OUT)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CS,   GPIO.OUT)
    
    # Pegel vorbereiten
    GPIO.output(CS,  GPIO.HIGH);
    GPIO.output(SCLK, GPIO.LOW);
    
    # Initialisierung des MCP23S17
    sendSPI(SPI_SLAVE_ADDR, SPI_PULLUP_A, 0xFF) # enable internal pullups
    sendSPI(SPI_SLAVE_ADDR, SPI_IODIRA, 0xFF) # GPPIOA als Eingaenge definieren
    sendSPI(SPI_SLAVE_ADDR, SPI_POL_A, 0xff) # invert logic
    sendSPI(SPI_SLAVE_ADDR, SPI_IODIRB, 0x00) # GPPIOB als Ausgaenge programmieren
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, 0x00) # Reset des GPIOB
    
    while True:
        for i in range(len(ledPattern)):
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern[i])
	    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA);
            print val
	    if (val != 0):
                start_new_thread(brake,(1,))
            time.sleep(0.01)

main()

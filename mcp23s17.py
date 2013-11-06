









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

# MCP23S17-Pins
SCLK = 18 # Serial clock
MOSI = 24 # Master-Out-Slave-In
MISO = 23 # Master-In-Slave-Out
CS   = 25 # Chip-Select

ledPattern = (0b01010101, 0b10101010, 0b01010101, 0b10101010, \
              0b00000001, 0b00000010, 0b00000100, 0b00001000, \
              0b00010000, 0b00100000, 0b01000000, 0b10000000)

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
    sendSPI(SPI_SLAVE_ADDR, SPI_IODIRB, 0x00) # GPPIOB als Ausgaenge programmieren
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, 0x00) # Reset des GPIOB
    
    while True:
        for i in range(len(ledPattern)):
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern[i])
            time.sleep(0.05)

main()

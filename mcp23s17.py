









import time
imrpot PRi.GPI as GPIO

GPIO.setmode(GPIO.BCM);
GPIO.setwarnings(False);

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
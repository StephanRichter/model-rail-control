#!/usr/bin/python
# coding=utf8
import time,sys
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

# initialize GPIO

GPIO.setmode(GPIO.BCM);
GPIO.setwarnings(False);

SCLK = 25 # Serial clock
MOSI = 18 # Master-Out-Slave-In
MISO = 23 # Master-In-Slave-Out
CS = 24 # Chip-Select

GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CS, GPIO.OUT)

GPIO.output(CS, GPIO.HIGH) # Pegel vorbereiten
GPIO.output(SCLK, GPIO.LOW); # Pegel vorbereiten

PULLUP_A = 0x0C
PULLUP_B = 0x0D
DIRECT_A = 0x00
DIRECT_B = 0x01
IN_POL_A = 0x02
IN_POL_B = 0x03

DEVICE_1 = 0<<1
DEVICE_2 = 1<<1

OPCODE=0x40
READ=1
WRITE=0

mode=READ

def sendValue(value):
	print 'sending ',
	print bin(value),
	print ':'
	# wert senden
	for i in range(8):
		if (value & 0x80):
			GPIO.output(MOSI, GPIO.HIGH)
		else:
			GPIO.output(MOSI, GPIO.LOW)
		# negative flanke des clocksignals generieren
		GPIO.output(SCLK, GPIO.HIGH)
		#sys.stdout.write(str(GPIO.input(MISO)))
		i=GPIO.input(MISO);
		sys.stdout.write(str(i))
		if i>0:
			sys.exit()
		GPIO.output(SCLK, GPIO.LOW)
		value <<=1 # Bitfolge eine Position nach links schieben
	print

def sendSPI(opcode, addr, data):
	# CS aktiv (LOW-Aktiv)
	print 'normal'
	GPIO.output(CS, GPIO.LOW)

	print 'addr 1'
	sendValue(0)
	sendValue(0)
	sendValue(0)
	GPIO.output(CS, GPIO.HIGH)
	time.sleep(0.01)
	print "dev 2"
	GPIO.output(CS, GPIO.LOW)
	sendValue(opcode|DEVICE_2)
	sendValue(addr)
	sendValue(data)

	GPIO.output(CS, GPIO.HIGH)

GPIO.output(CS, GPIO.LOW)

for i in range(0,20):
	sendValue(0xF0)
	GPIO.output(CS, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(CS, GPIO.LOW)

GPIO.output(CS, GPIO.HIGH)

# initialize the CHIP

#sendSPI(OPCODE|WRITE,PULLUP_A,0xFF) # enable pullup resistors for port A
#sendSPI(OPCODE|WRITE,PULLUP_B,0xFF) # enable pullup resistors for port B
#sendSPI(OPCODE|WRITE,DIRECT_A,0xFF) # set all ports of bank A as input
#sendSPI(OPCODE|WRITE,DIRECT_B,0xFF) # set all ports of bank B as input
#sendSPI(OPCODE|WRITE,IN_POL_A,0xFF) # invert logic on bank A
#sendSPI(OPCODE|WRITE,IN_POL_B,0xFF) # invert logic on bank B

#sendSPI(OPCODE|DEVICE_2|WRITE,PULLUP_A,0xFF) # enable pullup resistors for port A
#sendSPI(OPCODE|DEVICE_2|WRITE,PULLUP_B,0xFF) # enable pullup resistors for port B
#sendSPI(OPCODE|DEVICE_2|WRITE,DIRECT_A,0xFF) # set all ports of bank A as input
#sendSPI(OPCODE|DEVICE_2|WRITE,DIRECT_B,0xFF) # set all ports of bank B as input
#sendSPI(OPCODE|DEVICE_2|WRITE,IN_POL_A,0xFF) # invert logic on bank A
#sendSPI(OPCODE|DEVICE_2|WRITE,IN_POL_B,0xFF) # invert logic on bank B


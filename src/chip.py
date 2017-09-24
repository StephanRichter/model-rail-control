import time
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

class Chip(object):

    def send(self, value):
        # wert senden
        for i in range(8):
            if (value & 0x80):
                GPIO.output(self.mosi, GPIO.HIGH)
            else:
                GPIO.output(self.mosi, GPIO.LOW)
            # negative flanke des clocksignals generieren
            GPIO.output(self.clock, GPIO.HIGH)
            GPIO.output(self.clock, GPIO.LOW)
            value <<=1 # Bitfolge eine Position nach links schieben
        
    def sendSPI(self, register, data):
        GPIO.output(self.cable_select, GPIO.LOW)    # CS aktiv (LOW-Aktiv)    
        self.send(self.opcode)
        self.send(register)
        self.send(data)    
        GPIO.output(self.cable_select, GPIO.HIGH) # CS inaktiv    
        
        
    def readSPI(self):
        value = 0
                
        GPIO.output(self.cable_select, GPIO.LOW)    # CS aktiv (Low-Aktiv)
        self.send(self.opcode|0x01)
        self.send(0x12)
        for i in range(8):
            value <<= 1
            if (GPIO.input(self.miso)):
                value |= 0x01
            GPIO.output(self.clock, GPIO.HIGH)
            GPIO.output(self.clock, GPIO.LOW)
        GPIO.output(self.cable_select, GPIO.HIGH)# CS deaktivieren    
        
        GPIO.output(self.cable_select, GPIO.LOW)    # CS aktiv (Low-Aktiv)
        self.send(self.opcode|0x01)
        self.send(0x13)
        for i in range(8):
            value <<= 1
            if (GPIO.input(self.miso)):
                value |= 0x01
            GPIO.output(self.clock, GPIO.HIGH)
            GPIO.output(self.clock, GPIO.LOW)
        GPIO.output(self.cable_select, GPIO.HIGH)# CS deaktivieren    

        return value
        
    def activateAdressing(self):
        print " activating adressing for chip #{}".format(self.addr)
        self.sendSPI(0x0A, 0x08)
        self.sendSPI(0x0B, 0x08)
        
    def activatePullups(self):
        print " activating pullups for chip #{}".format(self.addr)
        self.sendSPI(0x0C, 0xFF) # Pullups (de)aktivieren    
        self.sendSPI(0x0D, 0xFF) # Pullups (de)aktivieren        
        
    def setDirection(self, dirA, dirB):
        print " setting directions for chip #{}".format(self.addr)
        self.sendSPI(0x00, dirA) # In/Out setzen
        self.sendSPI(0x01, dirB) # In/Out setzen
        
    def invertLogic(self):
        print " activating inverted logic for chip #{}".format(self.addr)
        self.sendSPI(0x02,0xFF) # Logik invertieren
        self.sendSPI(0x03,0xFF) # Logik invertieren        
    
    def __init__(self,addr,cable_select, clock, miso, mosi,input):
        print "Creating chip with address {}".format(addr);
        self.addr=addr
        self.opcode = addr<<1 | 0x40
        self.cable_select=cable_select
        self.clock=clock
        self.miso=miso
        self.mosi=mosi
        
        self.activateAdressing();
        self.activatePullups();
        if input:
            self.setDirection(0xff,0xff)
        else:
            self.setDirection(0x00,0xff)
        self.invertLogic()

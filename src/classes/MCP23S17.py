import time
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

class MCP23S17(object):

    def line(self,port,val):
        GPIO.output(port,val)
        time.sleep(0.00008)

    def send(self, value):
        # wert senden
        for i in range(8):
            self.line(self.clock, GPIO.LOW)
            if (value & 0x80):
                self.line(self.mosi, GPIO.HIGH)
            else:
                self.line(self.mosi, GPIO.LOW)
            # negative flanke des clocksignals generieren            
            self.line(self.clock, GPIO.HIGH)
            value <<=1 # Bitfolge eine Position nach links schieben            
        
    def sendSPI(self, register, data):
        self.line(self.cable_select, GPIO.LOW)    # CS aktiv (LOW-Aktiv)    
        self.send(self.opcode)
        self.send(register)
        self.send(data)    
        self.line(self.cable_select, GPIO.HIGH) # CS inaktiv    
        
        
    def readSPI(self):
        value = 0
                
        self.line(self.cable_select, GPIO.LOW)    # CS aktiv (Low-Aktiv)
        self.send(self.opcode|0x01)
        self.send(0x12)
        for i in range(8):
            value <<= 1
            if (GPIO.input(self.miso)):
                value |= 0x01
            self.line(self.clock, GPIO.HIGH)
            self.line(self.clock, GPIO.LOW)
        self.line(self.cable_select, GPIO.HIGH)# CS deaktivieren    
        
        self.line(self.cable_select, GPIO.LOW)    # CS aktiv (Low-Aktiv)
        self.send(self.opcode|0x01)
        self.send(0x13)
        for i in range(8):
            value <<= 1
            if (GPIO.input(self.miso)):
                value |= 0x01
            self.line(self.clock, GPIO.HIGH)
            self.line(self.clock, GPIO.LOW)
        self.line(self.cable_select, GPIO.HIGH)# CS deaktivieren    

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
        if input:
            self.setDirection(0xff,0xff)
            self.activatePullups();
            self.invertLogic()
        else:
            self.setDirection(0x00,0x00)        
    



if __name__ == "__main__":
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD);        
    GPIO.setwarnings(True);

    CS=13
    CLK=11
    MOSI=7
    MISO=5
    
    CS=7
    CLK=11
    MOSI=13
    MISO=15
    print "configuring line pins."
    GPIO.setup(CLK,  GPIO.OUT)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CS,   GPIO.OUT)
    
    print "initializing line level."
    self.line(CS,  GPIO.HIGH);
    self.line(CLK, GPIO.LOW);
    chip = MCP23S17(2,CS, CLK, MISO, MOSI,False)
    
    chip.sendSPI(0x13,0)
    chip.sendSPI(0x12,0)
    time.sleep(1)

    chip.sendSPI(0x13,0b11111111)
    chip.sendSPI(0x12,0b11111111)

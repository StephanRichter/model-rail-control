import time
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

class S88(object):

    def line(self,port,val):
        GPIO.output(port,val)
        time.sleep(0.0001)
        
    def readValue(self,):
        value = 0
                
        self.line(self.load,GPIO.HIGH)
        self.line(self.clock,GPIO.HIGH)
        self.line(self.clock,GPIO.LOW)
        if (GPIO.input(self.data)):
            value = 1;
        self.line(self.reset,GPIO.HIGH)
        self.line(self.reset,GPIO.LOW);
        self.line(self.load,GPIO.LOW);

        for i in range(self.contacts-1):
            self.line(self.clock,GPIO.HIGH)
            self.line(self.clock,GPIO.LOW)
            value <<= 1
            if (GPIO.input(self.data)):
                value |= 0x01

        return value
    
    
    def __init__(self,contacts,data,clock, reset, load):
        print "Creating S88 instance.";
        GPIO.setmode(GPIO.BOARD);        
        self.contacts=contacts
        self.data=data
        self.clock=clock
        self.reset=reset
        self.load=load
        GPIO.setup(data,GPIO.IN)
        GPIO.setup(clock,GPIO.OUT)
        GPIO.setup(reset,GPIO.OUT)
        GPIO.setup(load,GPIO.OUT)

if __name__ == "__main__":
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD);        
    GPIO.setwarnings(True);

    DATA=24
    RESET=16
    CLOCK=22
    LOAD=18
    
    chip = S88(16,DATA, CLOCK, RESET,LOAD)
   
    value = chip.readValue()

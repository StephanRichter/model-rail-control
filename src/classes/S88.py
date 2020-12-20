import time
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

class S88(object):

    def line(self,port,val):
        GPIO.output(port,val)
        time.sleep(0.00005)
        
    def readValue(self,):
        self.line(self.load,GPIO.HIGH)
        self.line(self.clock,GPIO.HIGH)
        self.line(self.clock,GPIO.LOW)
        value = GPIO.input(self.data)
        self.line(self.reset,GPIO.HIGH)
        self.line(self.reset,GPIO.LOW);
        self.line(self.load,GPIO.LOW);

        for i in range(1,self.contacts):
            self.line(self.clock,GPIO.HIGH)
            self.line(self.clock,GPIO.LOW)
            value |= GPIO.input(self.data)<<i

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

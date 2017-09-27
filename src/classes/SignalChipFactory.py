class SignalChipFactory(object):
    def __init__ (self,cable_select,clock,mosi,miso):
        self.cable_select = cable_select;
        self.clock = clock;
        self.mosi=mosi
        self.miso=miso
        print "setting board mode."
        GPIO.setmode(GPIO.BOARD);
        print "hiding warnings."
        GPIO.setwarnings(False);

        print "configuring line pins."
        GPIO.setup(clock,        GPIO.OUT)
        GPIO.setup(mosi,         GPIO.OUT)
        GPIO.setup(miso,         GPIO.IN)
        GPIO.setup(cable_select, GPIO.OUT)
        
        print "initializing line level."
        GPIO.output(cable_select,GPIO.HIGH);
        GPIO.output(clock,       GPIO.LOW);

    def provide(self,addr):
        return MCP23S17(addr,self.cable_select, self.clock, self.miso, self.mosi,False)
    
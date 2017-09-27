import time
from MCP23S17 import *
from SignalDriver import *
try:
    import RPi.GPIO as GPIO
except:
    print "Was not able to import GPIO"
    exit()

class SpiConnection(object):
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

    def sensor(self,addr):
        return MCP23S17(addr,self.cable_select, self.clock, self.miso, self.mosi,True)

    def signalDriver(self,addr):
        return SignalDriver(addr,self.cable_select, self.clock, self.miso, self.mosi)

    
from MCP23S17 import *

class SignalDriver(MCP23S17):
    RoGeGr=0
    
    def __init__(self,bus_addr,cable_select, clock, miso, mosi):
        self.nextSig=0
        self.signals={}
        MCP23S17.__init__(self,bus_addr,cable_select, clock, miso, mosi,False)

    def assign(self,addr,type):
        self.signals[addr] = (type,self.nextSig)
        if (type == SignalDriver.RoGeGr):
            self.nextSig+=3
        print self.signals
    
    def handle(self,addr,state):
        print self.signals
        print self.signals[addr]
        return True
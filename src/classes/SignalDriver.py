from MCP23S17 import *

class SignalDriver(MCP23S17):
    RoGeGr=0
    RoGr=1
    Off=0
    Rot=1
    Gelb=2
    Gruen=3
    def __init__(self,bus_addr,cable_select, clock, miso, mosi):
        self.nextSig=0
        self.signals={}
        self.state=0
        MCP23S17.__init__(self,bus_addr,cable_select, clock, miso, mosi,False)

    def assign(self,addr,type):
        self.signals[addr] = (type,self.nextSig)
        if (type == SignalDriver.RoGeGr):
            self.SignalRoGeGr(SignalDriver.Rot,self.nextSig)
            self.nextSig+=3
        elif (type == SignalDriver.RoGr):
            self.SignalRoGr(SignalDriver.Rot,self.nextSig)
            self.nextSig+=2
            
        
    def SignalRoGeGr(self,signal,shift):        
        #print 'SignalRoGeGr(state={}, shift={})'.format(signal,shift)        
        mod=0b111
        if signal==SignalDriver.Off:
            mod=0b000      
        if signal==SignalDriver.Rot:
            mod=0b001
        if signal==SignalDriver.Gelb:
            mod=0b110
        if signal==SignalDriver.Gruen:
            mod=0b100
        if mod != 0b111:
            dummy=0b1111111111111111
            mask=dummy<<3 # append 000
            for i in range(0,shift):
                mask=(mask<<1)|1
            self.state=self.state & mask | (mod<<shift)
            MCP23S17.sendSPI(self,0x13,self.state&0b11111111);
            MCP23S17.sendSPI(self,0x12,self.state>>8);
            #print format(self.state,'#018b');
            return True
        return False
        
    def SignalRoGr(self,signal,shift):        
        #print 'SignalRoGeGr(state={}, shift={})'.format(signal,shift)        
        mod=0b11
        if signal==SignalDriver.Off:
            mod=0b00      
        if signal==SignalDriver.Rot:
            mod=0b01
        if signal==SignalDriver.Gruen:
            mod=0b10
        if mod != 0b11:
            dummy=0b1111111111111111
            mask=dummy<<2 # append 00
            for i in range(0,shift):
                mask=(mask<<1)|1
            self.state=self.state & mask | (mod<<shift)
            MCP23S17.sendSPI(self,0x13,self.state&0b11111111);
            MCP23S17.sendSPI(self,0x12,self.state>>8);
            #print format(self.state,'#018b');
            return True
        return False

    
    def handle(self,addr,state,flag):
        if (flag == 0):
            return True

        print 'SignalDriver.handle(addr = {}, state={}, flag={})'.format(addr,state,flag)
        signal=self.signals[addr]
        
        type=signal[0]
        shift=signal[1]

        # TODO: check if entry exists
        
        if type == SignalDriver.RoGeGr:
            return self.SignalRoGeGr(state,shift)
        if type == SignalDriver.RoGr:
            return self.SignalRoGr(state,shift)

        
        return False

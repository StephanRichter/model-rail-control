# coding=utf8
import time
try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

class Loco:    
    def __init__(self,bus,addr,name,lenA,lenB):
        self.control=srcp.GL(bus,addr)
        self.control.init('N', '1', 128, 4)
        self.lenA=lenA
        self.lenB=lenB
        self.name=name
    
    def __str__(self):
        return self.name
    
    def appendA(self,train):
        for waggon in train:
            self.lenA+=waggon.len()
        print self.lenA
        
    def appendB(self,train):
        for waggon in train:
            self.lenB+=waggon.len()
        print self.lenB        
        
    def setSpeed(self,speed):
        print "Speed:",speed
        if speed<1:
            self.control.setDirection(0)
            self.control.send()
            time.sleep(1)
            self.control.setSpeed(-speed)
        else:
            self.control.setDirection(1)
            self.control.send()
            time.sleep(1)
            self.control.setSpeed(speed)
        self.control.send()
            
    def stop(self):
        print self.name,"stop!"
        self.control.setSpeed(0)
        self.control.send()
        time.sleep(0.1)
        self.control.setSpeed(0)
        self.control.send()
        time.sleep(0.1)
        self.control.setSpeed(0)
        self.control.send()
        
class Waggon:
    def __init__(self,length):
        self.length=length
        
    def len(self):
        return self.length
    
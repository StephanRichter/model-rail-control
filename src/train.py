# coding=utf8
try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

class Loco:    
    def __init__(self,bus,addr,name,lenA,lenB):
        self.control=srcp.GL(bus,addr)
        self.lenA=lenA
        self.lenB=lenB
        self.name=name
        control=None
    
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
        
    def stop(self):
        print self.name,"stop!"
        
    def setSpeed(self,speed):
        
        
class Waggon:
    def __init__(self,length):
        self.length=length
        
    def len(self):
        return self.length
    
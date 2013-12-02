# coding=utf8
from consts import UNDEFINED

class Platform:
    name="Platform"
    train=None
    station=UNDEFINED
    hasDecoupler=False
    bypass=None
    length=10000
    bypassLength=None
    platforms=set()
    
    def __init__(self,name,length=1000):
        self.name=name
        self.length=length
        
    def __str__(self):
        return self.name
    
    def setBypass(self,platform,length=0):
        self.hasDecoupler=True
        self.bypass=platform
        if (length==0):
            self.bypassLength=self.length
        else:
            self.bypassLength=length    
        
    def isFree(self):
        print self.name
        return self.train==None
    
    def setStation(self,station):
        self.station=station
    
    def setTrain(self,train):
        if self.train!=None:
            raise Exception(self.name+" not free!")
        self.train=train
# coding=utf8
from myconsts import *

class Platform:
    name="Platform"
    train=None
    station=UNDEFINED
    hasDecoupler=False
    bypass=None
    length=10000    
    bypassLength=UNDEFINED
    platforms=set()
    decoupleDirection=UNDEFINED
    targets=UNDEFINED
    
    def __init__(self,name,length=1000):
        self.name=name
        self.length=length
        self.targets=[]
        
    def __str__(self):
        return self.name
    
    def addTarget(self,platform):
        self.targets.append(platform)
    
    def setBypass(self,platform,length,direction):
        self.hasDecoupler=True
        self.bypass=platform
        self.bypassLength=length
        if direction==NACH_LINKS:
            self.decoupleDirection=NACH_RECHTS
        else:
            self.decoupleDirection=NACH_LINKS
        self.bypassDirection=direction    
        
    def isFree(self):
        print self.name
        return self.train==None
    
    def setStation(self,station):
        self.station=station
    
    def setTrain(self,train):
        if self.train!=None:
            raise Exception(self.name+" not free!")
        self.train=train

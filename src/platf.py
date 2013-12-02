# coding=utf8
from myconsts import *

class Platform:
    name="Platform"
    train=None
    station=UNDEFINED
    hasDecoupler=False
    length=10000    
    bypass=None
    bypassLength=UNDEFINED
    bypassDirection=UNDEFINED
    bypassSwitch=UNDEFINED
    platforms=set()
    decoupleDirection=UNDEFINED
    targets=UNDEFINED
    driveIn=UNDEFINED
    driveOut=UNDEFINED
    
    def __init__(self,name,length=1000):
        self.name=name
        self.length=length
        self.targets=[]
        
    def __str__(self):
        return self.name
    
    def addTarget(self,platform):
        self.targets.append(platform)
    
    def setBypass(self,platform,length,switchMethod,direction):
        self.hasDecoupler=True
        self.bypass=platform
        self.bypassLength=length
        self.bypassSwitch=switchMethod
        if direction==NACH_LINKS:
            self.decoupleDirection=NACH_RECHTS
        else:
            self.decoupleDirection=NACH_LINKS
        self.bypassDirection=direction    
        
    def isFree(self):
        return self.train==None
    
    def actuateDriveIn(self):
        self.driveIn()
        
    def actuateDriveOut(self):
        if self.driveOut==UNDEFINED:
            self.driveIn()
        else:
            self.driveOut()
    
    def actuateBypassSwitch(self):
        if self.bypassSwitch==UNDEFINED:
            raise Exception("No Bypass switch defined for "+self.name)
        else:
            self.bypassSwitch()
    
    def setDriveIn(self,method):
        self.driveIn=method
        
    def setDriveOut(self,method):
        self.driveOut=method
        
    def setFree(self):
        self.train=None
    
    def setStation(self,station):
        self.station=station
    
    def setTrain(self,train):
        if self.train!=None:            
            raise Exception(self.name+" not free!")
        self.train=train

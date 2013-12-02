# coding=utf8

class Platform:
    name="Platform"
    train=None
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
    
    def setBypass(self,platform,length):
        self.hasDecoupler=True
        self.bypass=platform
        self.bypassLength=length    
        
    def isFree(self):
        print self.name
        return self.train==None
    
    def setTrain(self,train):
        if self.train!=None:
            raise Exception(self.name+" not free!")
        self.train=train
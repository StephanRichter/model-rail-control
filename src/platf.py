# coding=utf8

class Platform:
    name="Platform"
    train=None
    hasDecoupler=False
    
    platforms=set()
    
    def __init__(self,name,decoupler=False):
        self.name=name
        self.hasDecoupler=decoupler
        
    def __str__(self):
        return self.name    
        
    def isFree(self):
        print self.name
        return self.train==None
    
    def setTrain(self,train):
        if self.train!=None:
            raise Exception(self.name+" not free!")
        self.train=train
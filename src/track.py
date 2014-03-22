class Track:
    
    def __init__(self,name):
        self.name=name
        self.connections=[]
        self.train=None
        self.contact=None
        self.turnouts=None
    
    def __str__(self):
        return self.name
        
    def connectTo(self,track):
        self.connections.append(track)
    
    def setTrain(self,train):
        self.train=train
    
    def getTrain(self):
        return self.train
    
    def getFreeTargets(self):
        targs=[]
        for trk in self.connections:
            if trk.getTrain()==None:
                targs.append(trk)
        return targs
    
    def setContact(self,contact):
        self.contact=contact
        
    def getContact(self):
        return self.contact
    
    def getTurnouts(self):
        return self.turnouts
    
    def setTurnouts(self,turnouts):
        self.turnouts=turnouts
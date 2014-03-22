class Track:
    name=None
    connections=[]
    
    def __init__(self,name):
        self.name=name
        
    def connectTo(self,track):
        self.connections.append(track)
        
    
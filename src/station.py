# coding=utf8
from platf import Platform

class Station:
    
    name="Station"
    
    platforms=[]
    
    def __init__(self,name):
        self.name=name
        
    def addPlatform(self,platform):
        self.platforms.append(platform)
        
    def freePlatforms(self):
        result=[]
        for platform in self.platforms:
            if platform.isFree():
                result.append(platform)
        return result
        
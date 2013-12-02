# coding=utf8
from platf import Platform
import time

class Station:
    
    name="Station"
    
    def __init__(self,name):
        self.name=name
        self.platforms=[]
        self.contacts=[]
        
    def __str__(self):
        return self.name
        
    def addContact(self,contact):
        self.contacts.append(contact)
    
    def addPlatform(self,platform):
        self.platforms.append(platform)
        
    def contact(self,num):
        if num in self.contacts:           
            for train in self.trains():
                train.contact(num)    
        
    def freePlatforms(self):
        result=[]
        for platform in self.platforms:
            if platform.isFree():
                result.append(platform)
        return result
        
    def trains(self):
        result=[]
        for platform in self.platforms:
            train=platform.train
            if train!=None:
                result.append(platform.train)
        return result
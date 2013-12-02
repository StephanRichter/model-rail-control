# coding=utf8
from platf import Platform
import time
from dummy_thread import start_new_thread

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
        platform.setStation(self)
        
    def freePlatforms(self):
        result=[]
        for platform in self.platforms:
            if platform.isFree():
                result.append(platform)
        return result
    
    def hasContact(self,contact):
        return contact in self.contacts
        
    def trains(self):
        result=[]
        for platform in self.platforms:
            train=platform.train
            if train!=None:
                result.append(platform.train)
        return result
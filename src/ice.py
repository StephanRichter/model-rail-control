# coding=utf8
from loco import *
from switches import *
import time

class ICE(Train):
    name = "  ICE"
    sp=40
    
    def ausfahrtRechts(self, delay=3):
        Train.ausfahrtRechts(self, delay)
        self.sleep(6)
        self.speed(128)
        self.sleep(9)
        self.einfahrt()
        self.speed(115)
        time.sleep(0.5)  
        self.speed(100)           

    def gleiswechsel(self, delay=3):
        Train.gleiswechsel(self, delay)
        self.speed(self.sp)
        print "GW"
    
# EVENTS

    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(6)          
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(100)
            time.sleep(0.5)
            self.speed(80)
            time.sleep(0.5)
            self.speed(60)
            time.sleep(0.5)
            self.speed(50)
            time.sleep(0.5)
            self.speed(40)
            time.sleep(1.5)
            self.speed(30)
            time.sleep(1.5)
            self.speed(20)
            time.sleep(1)
            self.speed(10)
            time.sleep(1)
            self.eingefahren()
            self.status=BEREIT
        elif (self.status==GLEISWECHSEL):
            time.sleep(2) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachLinks()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(self.sp)
            time.sleep(10.5) # hier anpassen
            self.stop()
            self.sleep(1)   
            self.platform.setFree()         
            self.setState(self.targetPlatform, BEREIT)
        else:
            time.sleep(2) 
            
    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(100)
            time.sleep(0.5)
            self.speed(80)
            time.sleep(0.5)
            self.speed(60)
            time.sleep(0.5)
            self.speed(40)
            time.sleep(1.5)
            self.speed(20)
            time.sleep(2.5)
            self.speed(10)
            if (self.targetPlatform.length==120):
                time.sleep(2.6)
            time.sleep(2)
            self.eingefahren()
            self.status=BEREIT
        elif (self.status==GLEISWECHSEL):
            time.sleep(4) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(self.sp)
            if self.targetPlatform==r1 or self.targetPlatform==r2:
                time.sleep(16) # hier anpassen
            else:
                time.sleep(13.5) # hier anpassen
            self.stop()   
            self.platform.setFree()         
            self.setState(self.targetPlatform, BEREIT)
        else:
            time.sleep(2) 

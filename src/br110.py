# coding=utf8
from train import *
import time,os,srcp
from switches import *

class BR110(Train):
    
    name = "BR110"
    
    def ausfahrtRechts(self, delay=3):
        Train.ausfahrtRechts(self, delay=delay)
        self.sleep(16)
        self.speed(128)
        self.sleep(20)
        self.einfahrt()
    
# Events

    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(15)            
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(60)
            if (self.trainlength==82):
                time.sleep(12)
                self.speed(20)
                time.sleep(4)
            else:
                raise Exception("keine Einfahrt definiert für Zuglänge =",self.trainlength)                
            time.sleep(1)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            self.stop()
            time.sleep(1)
            self.nachLinks()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(20)
            time.sleep(40) # hier anpassen
            self.stop()
            self.sleep(1)   
            self.status=BEREIT 

    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            if (self.trainlength==82):
                time.sleep(9)
                self.speed(20)
            time.sleep(3)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            time.sleep(13) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(20)
            if (self.targetPlatform==r1 or self.targetPlatform==r2):
                time.sleep(45) # hier anpassen
            else:
                time.sleep(46) # hier anpassen
            self.stop()   
            self.status=BEREIT
# coding=utf8
from train import *
import time,os,srcp
from switches import *

class BR118(Train):
    name = "BR118"
    
    def abkuppelnLinks(self,delay):
        print "BR 118 startet abkuppeln links in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
    
    def abkuppelnRechts2(self,delay=3):
        print "BR 118 startet abkuppeln auf Gleis 2, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.trainlength==100):
            self.nachLinks()
            time.sleep(1)
            self.speed(10)
            time.sleep(1.5)
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            self.stop()
            time.sleep(0.1)
            entkuppeln2()
            time.sleep(0.1)
            self.nachRechts()
            time.sleep(0.1)
            entkuppeln2()
            self.speed(20)
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            entkuppeln2()
            self.sleep(3.6)
            self.stop()
            self.status=ABGEKUPPELT
        else:
            print "Abkuppelvorgang für Zuglänge (",self.trainlength,") nicht definiert"  
        
    def ankuppelnLinks(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Train.ankuppeln(self, delay)
        if (self.trainlength==100):
            time.sleep(12)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
    
    def ankuppelnRechts(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Train.ankuppeln(self, delay)
        if (self.targetPlatform==r2):
            if (self.trainlength==100):
                time.sleep(17)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
        
    def ausfahrtRechts(self, delay=3):
        Train.ausfahrtRechts(self, delay)
        self.sleep(5)
        self.speed(128)
        self.sleep(16)
        self.einfahrt()

# events

    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(12)            
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(60)
            if (self.targetPlatform==r1):
                if (self.trainlength==100):
                    time.sleep(10)
                    self.speed(20)
                    time.sleep(4)
            time.sleep(1)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            if (self.trainlength==100):
                time.sleep(23) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachLinks()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(20)
            time.sleep(45) # hier anpassen
            self.stop()
            self.sleep(1)
            self.platform.setFree()         
            self.setState(self.targetPlatform, BEREIT)
        elif (self.status==UMFAHREN):
            self.stop()          
            self.sleep(1)  
            self.status=ANKUPPELN
            self.nachLinks()
            self.ankuppelnLinks(WENDEZEIT)

    
    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            if self.targetPlatform==r3 or self.targetPlatform==r2:
                if (self.trainlength==100):
                    time.sleep(9)
                    self.speed(20)
                    return # Dieser Zug ist zu lang und muss über den Reedkontakt beim Entkuppler hinausfahren
            time.sleep(1)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            if (self.trainlength==100):
                time.sleep(24) # hier anpassen
            else:
                print "Gleiswechsel nicht definiert für zuglänge =",self.trainlength
                self.status=UNDEFINED
                return
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.nachRechts()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(20)
            if self.targetPlatform==r1 or self.targetPlatform==r2:
                if (self.trainlength==100):
                    time.sleep(49) # hier anpassen
                else:
                    print "Gleiswechsel nicht definiert für zuglänge =",self.trainlength
                    self.status=UNDEFINED
                    return
            else:
                if (self.trainlength==100):
                    time.sleep(53) # hier anpassen
                else:
                    print "Gleiswechsel nicht definiert für zuglänge =",self.trainlength
                    self.status=UNDEFINED
                    return
            self.stop()   
            self.platform.setFree()         
            self.setState(self.targetPlatform, BEREIT)
        elif (self.status==UMFAHREN):
            self.stop()
            self.status=ANKUPPELN
            self.ankuppelnRechts(WENDEZEIT)
        elif (self.status==NACH_RECHTS):
            pass
            
    def entkupplerLinksEvent(self):
        if (self.status==ABKUPPELN):
            time.sleep(3.7) # Überfahren
            self.stop()
            time.sleep(WENDEZEIT)
        
            self.nachRechts() # Anrücken
            self.speed(10)
            time.sleep(0.6)
            entkupplenLinks(3)
            self.stop()        
            time.sleep(0.1)
            self.nachLinks()
            time.sleep(0.1)
            self.speed(25)
            entkupplenLinks(3)
            time.sleep(4.1)        
            self.stop()
            time.sleep(1)
            self.status=ABGEKUPPELT
            
    def entkupplerRechts2Event(self):
        if (self.status==EINFAHRT):
            time.sleep(3.3)
            self.eingefahren()


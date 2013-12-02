# coding=utf8
import time,os,srcp
import myconsts
import environ
from switches import *
from train import *

class BR86(Train):
    name = " BR86"
            
    def abkuppelnLinks(self,delay):
        print "BR 86 startet abkuppeln links in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
        
    def abkuppelnRechts2(self,delay=3):
        print "BR 86 startet abkuppeln auf Gleis 2, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.trainlength==55):
            self.nachRechts()
            time.sleep(1)
            self.speed(20)            
        else:
            print "ABkuppelvorgang für Zuglänge (",self.trainlength,") nicht definiert"  
        
    def abkuppelnRechts3(self,delay=3):
        print "BR 86 startet abkuppeln auf Gleis 3, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.trainlength==55):
            self.nachRechts()
            time.sleep(1)
            self.speed(20)            
        else:
            print "Abkuppelvorgang für Zuglänge (",self.trainlength,") nicht definiert"  

    def ankuppelnLinks(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        self.nachLinks()
        Train.ankuppeln(self, delay)
        if (self.trainlength==55):
            time.sleep(24)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
        
    def ankuppelnRechts(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        self.nachRechts()
        self.nachRechts()
        Train.ankuppeln(self, delay)
        if (self.platform==r2):
            if (self.trainlength==55):
                time.sleep(21)
            else:
                print "kein Ankuppeln definiert für Zuglänge =",self.trainlength
                self.status=UNDEFINED
        elif (self.platform==r3):
            if (self.trainlength==55):
                time.sleep(20)
            else:
                print "kein Ankuppeln definiert für Zuglänge =",self.trainlength
                self.status=UNDEFINED
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
    
    def ausfahrtRechts(self, delay=3):
        Train.ausfahrtRechts(self, delay=delay)
        self.sleep(16)
        self.speed(128)
        self.sleep(14)
        self.einfahrt()

# events
        
    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(17)            
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(60)
            if (self.targetPlatform==r1):
                if (self.trainlength==55):
                    time.sleep(13)
                    self.speed(20)
                    time.sleep(3)
            time.sleep(1)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            if (self.trainlength==55):
                time.sleep(9)
            self.stop()
            time.sleep(1)
            self.nachLinks()
            self.targetPlatform.actuateDriveIn()      
            time.sleep(WENDEZEIT)
            self.speed(20)
            time.sleep(29)
            self.stop()
            self.sleep(1)   
            self.platform=self.targetPlatform
            self.targetPlatform.setFree()
            self.status=BEREIT         
        elif (self.status==UMFAHREN):
            self.stop()          
            self.sleep(1)  
            self.status=ANKUPPELN            
            self.ankuppelnLinks(WENDEZEIT)

    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            if (self.trainlength==55):
                time.sleep(9)
                self.speed(20)
            time.sleep(10)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            time.sleep(12)
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.targetPlatform.actuateDriveIn()
            time.sleep(WENDEZEIT)
            self.speed(20)
            if (self.targetPlatform==r1 or self.targetPlatform==r2):
                time.sleep(32)
            else:
                time.sleep(36)
            self.stop()   
            self.platform=self.targetPlatform
            self.targetPlatform.setFree()
            self.status=BEREIT
        elif (self.status==UMFAHREN):
            self.stop()
            self.status=ANKUPPELN            
            self.ankuppelnRechts(WENDEZEIT)


    def entkupplerLinksEvent(self):
        if (self.status==ABKUPPELN):
            time.sleep(5.6) # Überfahren
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
            time.sleep(4.2)        
            self.stop()
            time.sleep(1)
            self.status=ABGEKUPPELT

    def entkupplerRechts2Event(self):
        if (self.status==ABKUPPELN):
            self.stop()
            time.sleep(1)
            self.nachLinks()
            time.sleep(1)
            self.speed(10)
            time.sleep(0.9)
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
        elif (self.status==EINFAHRT):
            time.sleep(3.2)
            self.eingefahren()

    def entkupplerRechts3Event(self):
        if (self.status==ABKUPPELN):
            self.stop()
            time.sleep(1)
            self.nachLinks()
            time.sleep(1)
            self.speed(10)
            time.sleep(0.9)
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            self.stop()
            time.sleep(0.1)
            entkuppeln3()
            time.sleep(0.1)
            self.nachRechts()
            time.sleep(0.1)
            entkuppeln3()
            self.speed(20)
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            self.sleep(3.6)
            self.stop()
            self.status=ABGEKUPPELT  
        elif (self.status==EINFAHRT):
            time.sleep(3.2)
            self.eingefahren()

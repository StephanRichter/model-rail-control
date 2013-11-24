# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR118(Lok):
    name = "BR 118"
    
    def abkuppelnLinks(self,delay):
        print "BR 118 startet abkuppeln links in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
        
    def ankuppelnLinks(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Lok.ankuppelnLinks(self, delay)
        if (self.zuglaenge==100):
            time.sleep(11)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
    
    def ankuppelnRechts(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Lok.ankuppelnRechts(self, delay)
        if (self.nachGleis==2):
            if (self.zuglaenge==100):
                time.sleep(17)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.vonGleis=self.nachGleis
        self.status=BEREIT
        
    def ausfahrtRechts(self, delay=3):
        Lok.ausfahrtRechts(self, delay=delay)
        self.sleep(3)
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
            print self.nachGleis
            print self.zuglaenge
            if (self.nachGleis==1):
                if (self.zuglaenge==100):
                    time.sleep(10)
                    self.speed(20)
                    time.sleep(4)
            time.sleep(1)
            self.eingefahren()
        elif (self.status==UMFAHREN):
            self.stop()          
            self.sleep(1)  
            self.status=ANKUPPELN
            self.ankuppelnLinks(WENDEZEIT)

    
    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            if (self.nachGleis==3 or self.nachGleis==2):
                if (self.zuglaenge==100):
                    time.sleep(9)
                    self.speed(20)
                    return # Dieser Zug ist zu lang und muss über den Reedkontakt beim Entkuppler hinausfahren
            time.sleep(1)
            self.eingefahren()
        elif (self.status==UMFAHREN):
            self.stop()
            self.status=ANKUPPELN
            self.ankuppeln(WENDEZEIT)
        else:
            self.stop()
            self.status=UNDEFINED
            
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
            time.sleep(3.2)
            self.eingefahren()


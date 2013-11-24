# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR86(Lok):
    name = "BR 86 "
    
        
    def abkuppelnLinks(self,delay):
        print "BR 86 startet abkuppeln links in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
        
    def abkuppelnRechts2(self,delay=3):
        print "BR130 startet abkuppeln auf Gleis 2, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.zuglaenge==55):
            self.nachRechts()
            time.sleep(1)
            self.speed(20)            
        else:
            print "ABkuppelvorgang für Zuglänge (",self.zuglaenge,") nicht definiert"  
        
    def ankuppelnLinks(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Lok.ankuppelnLinks(self, delay)
        if (self.zuglaenge==55):
            time.sleep(24)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
        
    def ankuppelnRechts(self, delay=3): # kein print hier, das macht schon die aufgerufene Supermethode
        Lok.ankuppelnRechts(self, delay)
        if (self.nachGleis==2):
            if (self.zuglaenge==55):
                time.sleep(20)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.vonGleis=self.nachGleis
        self.status=BEREIT
    
    def ausfahrtRechts(self, delay=3):
        Lok.ausfahrtRechts(self, delay=delay)
        self.sleep(16)
        self.speed(128)
        self.sleep(14)
        self.einfahrt()
        

# events
        
    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            if (self.nachGleis==3 or self.nachGleis==2):
                if (self.zuglaenge==55):
                    time.sleep(9)
                    self.speed(20)
            time.sleep(10)
            self.eingefahren()
        elif (self.status==GLEISWECHSEL):
            time.sleep(18)
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.einfahrWeichenRechts()
            time.sleep(WENDEZEIT)
            self.speed(20)
            if (self.nachGleis==1 or self.nachGleis==2):
                time.sleep(38)
            else:
                time.sleep(42)
            self.stop()   
            self.vonGleis=self.nachGleis
            self.status=BEREIT         
            
        elif (self.status==UMFAHREN):
            self.stop()
            self.status=ANKUPPELN
            self.ankuppeln(WENDEZEIT)

    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(17)            
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(60)
            if (self.nachGleis==1):
                if (self.zuglaenge==55):
                    time.sleep(11)
                    self.speed(20)
                    time.sleep(3)
            time.sleep(1)
            self.eingefahren()
        elif (self.status==UMFAHREN):
            self.stop()          
            self.sleep(1)  
            self.status=ANKUPPELN
            self.ankuppelnLinks(WENDEZEIT)

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

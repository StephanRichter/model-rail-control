# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR130(Lok):
    name = "BR 130"
    
    def abkuppelnLinks(self,delay):
        print "BR130 startet abkuppeln links in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
        
    def abkuppelnRechts2(self,delay=3):
        print "BR130 startet abkuppeln auf Gleis 2, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.zuglaenge==82):
            self.nachLinks()
            time.sleep(1)
            self.speed(10)
            time.sleep(0.5)
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

    def abkuppelnRechts3(self,delay=3):
        print "BR130 startet abkuppeln auf Gleis 3, rechts, in",delay,"Sekunden"
        time.sleep(delay)
        if (self.zuglaenge==82):
            self.nachLinks()
            time.sleep(1)
            self.speed(10)
            time.sleep(1)
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            self.stop()
            time.sleep(0.1)
            self.nachRechts()
            time.sleep(0.1)
            self.speed(20)
            entkuppeln3()
            entkuppeln3()
            entkuppeln3()
            self.sleep(3.6)
            self.stop()
            self.status=ABGEKUPPELT           

    def ankuppelnLinks(self, delay=3):
        Lok.ankuppelnLinks(self, delay)
        if (self.zuglaenge==82):
            time.sleep(13)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.status=BEREIT
        
    def ankuppelnRechts(self, delay=3):
        print "BR130 startet ankuppeln rechts in",delay,"Sekunden"
        Lok.ankuppelnRechts(self, delay)
        if (self.nachGleis==2):
            if (self.zuglaenge==82):
                time.sleep(15)
        elif (self.nachGleis==3):        
            if (self.zuglaenge==82):
                time.sleep(17)
        self.stop()
        time.sleep(3)
        self.lichtAus()
        self.vonGleis=self.nachGleis
        self.status=BEREIT
            
    def ausfahrtRechts(self, delay=3):
        Lok.ausfahrtRechts(self, delay=delay)
        self.sleep(16)
        self.speed(128)
        self.sleep(12)
        self.einfahrt()
                
# ========== events ===========>
    
    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(12)            
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(60)
            if (self.nachGleis==1):
                if (self.zuglaenge==82):
                    time.sleep(6)
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
                if (self.zuglaenge==82):
                    time.sleep(9)
                    self.speed(20)
                    return # Dieser Zug ist zu lang und muss über den Reedkontakt beim Entkuppler hinausfahren
            time.sleep(1)
            self.eingefahren()
        elif (self.status==UMFAHREN):
            self.stop()
            self.status=ANKUPPELN
            self.ankuppeln(WENDEZEIT)

    def entkupplerLinksEvent(self):
        if (self.status!=ABKUPPELN):
            self.stop()
            self.status=UNDEFINED
            return        
        time.sleep(2) # Überfahren
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
        time.sleep(3.5)        
        self.stop()
        time.sleep(1)
        self.status=ABGEKUPPELT
        
    def entkupplerRechts2Event(self):
        if (self.status==EINFAHRT):
            time.sleep(3.2)
            self.eingefahren()
            
    def entkupplerRechts3Event(self):
        if (self.status==EINFAHRT):
            time.sleep(3.2)
            self.eingefahren()

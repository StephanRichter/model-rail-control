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
        
    def entkupplerLinksEvent(self):
        print "Kontakt!"
        if (self.status!=ABKUPPELN):
            self.stop()
            self.status=UNDEFINED
            return        
        time.sleep(2) # Überfahren
        self.stop()
        time.sleep(WENDEZEIT)
        
        self.nachRechts() # Anrücken
        self.speed(10)
        time.sleep(0.8)
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
        self.status=UMFAHREN
        
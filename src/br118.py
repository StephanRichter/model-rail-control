# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR118(Lok):
    name = "BR 118"
    
    def ankuppelnRechts(self, delay=3):
        print "BR130 startet ankuppeln rechts in",delay,"Sekunden"
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
        else:
            self.stop()
            self.status=UNDEFINED
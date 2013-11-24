# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR86(Lok):
    name = "BR 86 "
    
    def ausfahrtRechts(self, delay=3):
        Lok.ausfahrtRechts(self, delay=delay)
        self.sleep(16)
        self.speed(128)
        self.sleep(14)
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

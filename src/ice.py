# coding=utf8
from lok import *
from weichen import *
import time

class ICE(Lok):
    name = "ICE   "
    
# EVENTS

    def einfahrtLinksEvent(self):
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(7)            
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
        elif (self.status==GLEISWECHSEL):
            time.sleep(4) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachLinks()            
            if (self.nachGleis==1):
                bahnhofLinksGerade()
            elif (self.nachGleis==2):
                bahnhofLinksAbzweig()
            else:
                print "es gibt kein Gleis",self.nachGleis,"im linken Bahnhof"
                return
            time.sleep(WENDEZEIT)
            self.speed(20)
            time.sleep(18) # hier anpassen
            self.stop()
            self.sleep(1)   
            self.vonGleis=self.nachGleis
            self.status=BEREIT         

    def einfahrtRechtsEvent(self):
        if (self.status==EINFAHRT):
            self.speed(60)
            time.sleep(3)
            self.speed(20)
            if (self.nachGleis>2):
                time.sleep(2)
            time.sleep(2)
            self.eingefahren()
            self.status=BEREIT
        elif (self.status==GLEISWECHSEL):
            time.sleep(6) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.einfahrWeichenRechts()
            time.sleep(WENDEZEIT)
            self.speed(20)
            if (self.nachGleis<3):
                time.sleep(21) # hier anpassen
            elif (self.nachGleis==3 or self.nachGleis==4):
                time.sleep(23) # hier anpassen
            self.stop()   
            self.vonGleis=self.nachGleis
            self.status=BEREIT 
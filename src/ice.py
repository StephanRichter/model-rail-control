# coding=utf8
from lok import *
from weichen import *
import time

class ICE(Lok):
    name = "ICE   "
    sp=40
    
    def ausfahrtRechts(self, delay=3):
        Lok.ausfahrtRechts(self, delay)
        self.sleep(6)
        self.speed(128)
        self.sleep(8)
        self.einfahrt()
        self.speed(100)  

        
    def gleiswechsel(self, delay=3):
        Lok.gleiswechsel(self, delay)
        self.speed(self.sp)
        print "GW"
    
# EVENTS

    def einfahrtLinksEvent(self):
        print "EKL"
        if (self.bahnhof!=LINKS):
            time.sleep(2)
            return
        if (self.status==AUSFAHRT):
            self.speed(128)
            self.status=NACH_RECHTS
            time.sleep(6)          
            self.einfahrt()
        elif (self.status==EINFAHRT):
            self.speed(100)
            time.sleep(0.5)
            self.speed(80)
            time.sleep(0.5)
            self.speed(60)
            time.sleep(0.5)
            self.speed(50)
            time.sleep(0.5)
            self.speed(40)
            time.sleep(1.5)
            self.speed(30)
            time.sleep(1.5)
            self.speed(20)
            time.sleep(1)
            self.speed(10)
            time.sleep(1)
            self.eingefahren()
            self.status=BEREIT
        elif (self.status==GLEISWECHSEL):
            time.sleep(2) # hier anpassen
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
            self.speed(self.sp)
            time.sleep(10.5) # hier anpassen
            self.stop()
            self.sleep(1)   
            self.vonGleis=self.nachGleis
            self.status=BEREIT         
        else:
            time.sleep(2) 
            
    def einfahrtRechtsEvent(self):
        print "EKR"
        if (self.bahnhof!=RECHTS):
            time.sleep(2)
            return
        if (self.status==EINFAHRT):
            self.speed(100)
            time.sleep(0.5)
            self.speed(80)
            time.sleep(0.5)
            self.speed(60)
            time.sleep(0.5)
            self.speed(40)
            time.sleep(1.5)
            self.speed(20)
            time.sleep(2.5)
            self.speed(10)
            if (self.nachGleis>2):
                time.sleep(2)
            time.sleep(2)
            self.eingefahren()
            self.status=BEREIT
        elif (self.status==GLEISWECHSEL):
            time.sleep(4) # hier anpassen
            self.stop()
            time.sleep(1)
            self.nachRechts()            
            self.einfahrWeichenRechts()
            time.sleep(WENDEZEIT)
            self.speed(self.sp)
            if (self.nachGleis<3):
                time.sleep(16) # hier anpassen
            elif (self.nachGleis==3 or self.nachGleis==4):
                time.sleep(13.5) # hier anpassen
            self.stop()   
            self.vonGleis=self.nachGleis
            self.status=BEREIT
        else:
            time.sleep(2) 

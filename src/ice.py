# coding=utf8
from lok import *
from weichen import *
import time

class ICE(Lok):
    
    def von3nachLinks1(self,delay=1):        
        print "ICE startet nach links 1 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt4()
        time.sleep(1)
        self.speed(128)
        time.sleep(19)
        self.speed(80)
        time.sleep(1)
        self.speed(60)
        time.sleep(1)
        self.speed(40)
        time.sleep(1)
        self.speed(20)
        time.sleep(1)
        self.stop()
        self.status=Lok.BEREIT_LINKS1
        time.sleep(15)
        self.lichtAus()      
        
    def von1nachRechts3(self,delay=1):
        print "ICE startet nach rechts 3 in",delay,"sekunden"
        self.direction(1)
        time.sleep(1)
        self.lichtAn()
        time.sleep(1)
        time.sleep(delay-1)
        time.sleep(1)
        self.speed(50)
        time.sleep(8)
        self.speed(128)
        time.sleep(7)
        einfahrt4()
   
    def einfahrtRechtsEvent(self):
        if (self.status==Lok.NACH_RECHTS3):
            time.sleep(1)
            self.speed(100)
            time.sleep(1)
            self.speed(50)
            time.sleep(2)
            self.stop()
            self.status=Lok.BEREIT_RECHTS3
            time.sleep(15)
            self.lichtAus()
        else:
            self.stop()            


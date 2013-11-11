# coding=utf8
from lok import *
from weichen import *
import time
from kontakte import EINFAHRT_RECHTS

class ICE(Lok):
    
    def einfahrtLinks(self):
        print "ICE: Einfahrt links"
        self.speed(50)
        time.sleep(3)
        self.speed(30)
        time.sleep(2)
        self.stop()
        self.status=BEREIT_LINKS1
            
    def einfahrt3(self):
        print "ICE: Einfahrt rechts (Gleis 3)"
        self.status=EINFAHRT_RECHTS
        self.speed(50)
        time.sleep(2)
        self.stop()
        self.status=BEREIT_RECHTS3
        time.sleep(15)
        self.lichtAus()
            
    def einfahrt4(self):
        print "ICE: Einfahrt rechts (Gleis 4)"
        self.status=EINFAHRT_RECHTS
        self.speed(50)
        time.sleep(2)
        self.stop()
        self.status=BEREIT_RECHTS4
        time.sleep(15)
        self.lichtAus()
    
    def von3nachLinks1(self,delay=1):        
        print "ICE startet nach links 1 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt3()
        time.sleep(1)
        self.speed(128)
        
    def von4nachLinks1(self,delay=1):        
        print "ICE startet nach links 1 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt4()
        time.sleep(1)
        self.speed(128)
        time.sleep(8)
        self.status=EINFAHRT_LINKS1
        
    def von1nachRechts3(self,delay=1):
        print "ICE startet nach rechts 3 in",delay,"sekunden"
        self.direction(1)
        time.sleep(1)
        self.lichtAn()
        time.sleep(1)
        time.sleep(delay)
        self.speed(50)

    def von1nachRechts4(self,delay=1):
        print "ICE startet nach rechts 4 in",delay,"sekunden"
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
        if (self.status==NACH_RECHTS3):
            einfahrt3()
        elif (self.status==NACH_RECHTS4):
            einfahrt4()
        else:
            self.stop()
            
    def einfahrtLinksEvent(self):
        if (self.status==NACH_RECHTS4):
            self.speed(128)            
            time.sleep(7)
            einfahrt3()
        elif (self.status==EINFAHRT_LINKS1):
            self.einfahrtLinks()



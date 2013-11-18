# coding=utf8
from lok import *
from weichen import *
import time

class ICE(Lok):
    name = "ICE   "
    def einfahrtLinks1(self):
        print "ICE: Einfahrt links 1"
        self.speed(50)
        time.sleep(3)
        self.speed(30)
        time.sleep(3)
        self.stop()
        self.status=BEREIT_LINKS1
        time.sleep(15)
        self.lichtAus()
            
    def einfahrtLinks2(self):
        print "ICE: Einfahrt links 2"
        self.speed(50)
        time.sleep(3)
        self.speed(30)
        time.sleep(2)
        self.stop()
        self.status=BEREIT_LINKS2
        time.sleep(15)
        self.lichtAus()

    def einfahrt1(self):
        print "ICE: Einfahrt rechts (Gleis 1)"
        self.status=EINFAHRT_RECHTS1
        self.speed(60)
        time.sleep(3)
        self.speed(40)
        time.sleep(1)
        self.speed(20)
        time.sleep(2)
        self.stop()
        self.status=BEREIT_RECHTS1
        time.sleep(15)
        self.lichtAus()

    def einfahrt3(self):
        print "ICE: Einfahrt rechts (Gleis 3)"
        self.status=EINFAHRT_RECHTS3
        self.speed(60)
        time.sleep(3)
        self.speed(40)
        time.sleep(1)
        self.speed(20)
        time.sleep(1)
        self.speed(10)
        time.sleep(1)
        self.stop()
        self.status=BEREIT_RECHTS3
        time.sleep(15)
        self.lichtAus()
            
    def einfahrt4(self):
        print "ICE: Einfahrt rechts (Gleis 4)"
        self.status=EINFAHRT_RECHTS4
        self.speed(60)
        time.sleep(3)
        self.speed(40)
        time.sleep(1)
        self.speed(20)
        time.sleep(1)
        self.speed(10)
        time.sleep(1)
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
        
    def von1nachLinks(self,delay=1):        
        print "ICE startet von Gleis 1 nach links in",delay,"sekunden"
        self.direction(LINKS)
        time.sleep(1)
        self.lichtAn()
        time.sleep(delay)
        ausfahrt1()
        time.sleep(3)
        self.speed(128)
        time.sleep(8)
        if (self.status==NACH_LINKS1):
            bahnhofLinksGerade()
            self.status=EINFAHRT_LINKS1
        elif (self.status==NACH_LINKS2):
            bahnhofLinksAbzweig()
            self.status=EINFAHRT_LINKS2

    def von1nachLinks2(self,delay=1):        
        print "ICE startet nach links 2 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt1()
        time.sleep(1)
        self.speed(128)
        time.sleep(8)
        bahnhofLinksAbzweig()
        self.status=EINFAHRT_LINKS2

    def von4nachLinks2(self,delay=1):        
        print "ICE startet nach links 2 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt4()
        time.sleep(1)
        self.speed(128)
        time.sleep(8)
        bahnhofLinksAbzweig()
        self.status=EINFAHRT_LINKS2
        
    def von2nachRechts(self,delay=1):
        print "ICE startet nach rechts 1 in",delay,"sekunden"
        self.direction(RECHTS)
        time.sleep(1)
        self.lichtAn()
        time.sleep(1)
        time.sleep(delay)
        bahnhofLinksAbzweig()
        time.sleep(2)
        self.speed(50)

    def von1nachRechts(self,delay=1):
        print "ICE startet nach rechts in",delay,"sekunden"
        self.direction(RECHTS)
        time.sleep(1)
        self.lichtAn()
        time.sleep(1)
        time.sleep(delay)
        self.speed(50)
   
    def einfahrtRechtsEvent(self):
        if (self.status==NACH_RECHTS1):
            self.einfahrt1() # Abbremsen
        if (self.status==NACH_RECHTS3):
            self.einfahrt3() # Abbremsen
        elif (self.status==NACH_RECHTS4):
            self.einfahrt4() # Abbremsen
            
    def einfahrtLinksEvent(self):
        if (self.status==NACH_RECHTS1):
            self.speed(128)            
            time.sleep(7)
            einfahrt1() # Weichenstraße
        elif (self.status==NACH_RECHTS4):
            self.speed(128)            
            time.sleep(7)
            einfahrt4() # Weichenstraße

        elif (self.status==EINFAHRT_LINKS1):
            self.einfahrtLinks1()
        elif (self.status==EINFAHRT_LINKS2):
            self.einfahrtLinks2()



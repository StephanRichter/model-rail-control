# coding=utf8
from lok import *
import time,os,srcp
from weichen import ausfahrt3, weiche10, entkupplenLinks,\
    bahnhofLinksGerade, einfahrt3, entkuppler3, weiche34, einfahrt4

class BR110(Lok):
    
    wendezug = True
    name = "BR 110"   
    def ankuppeln1(self):
        print "BR 110 Ankuppeln auf Gleis 1 (links)"
        self.status=ANKUPPELN        
        self.direction(LINKS)
        time.sleep(1)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(60)
        time.sleep(8)
        self.speed(20)
        time.sleep(11)
        self.stop()
        self.status=BEREIT_LINKS1
        
    def ankuppeln3(self):
        print "BR 110 Ankuppeln auf Gleis 3 (rechts)"
        time.sleep(1)
        einfahrt3()
        time.sleep(2)
        self.direction(1)
        time.sleep(2)
        self.speed(60)
        time.sleep(11)
        self.speed(20)
        time.sleep(2)
        self.speed(5)
        time.sleep(5)
        self.stop()
        self.status=BEREIT_RECHTS3
        
    def einfahrtLinks(self):
        print "BR 110 fährt auf Gleis 1 (links) ein"
        self.speed(100)
        time.sleep(4)
        self.speed(80)
        time.sleep(2)
        self.speed(60)
        time.sleep(2)
        self.speed(40)
        time.sleep(4)
        self.speed(20)
        time.sleep(4)
        self.stop()
        if (self.wendezug):
            self.status=BEREIT_LINKS1
        else:
            self.status=EINGEFAHREN_LINKS1

    def einfahrtRechts3(self):
        print "BR 110 fährt auf Gleis 3 (rechts) ein"
        if (self.wendezug):
            pass
        else:
            time.sleep(2)          
            self.speed(100)            
            time.sleep(3)
            self.speed(80)
            
        time.sleep(2)
        self.speed(60)
        time.sleep(2)
        self.speed(40)
        time.sleep(7)
        self.speed(20)
        time.sleep(2)
        self.stop()
        time.sleep(1)
        if (self.wendezug):
            self.status=BEREIT_RECHTS3
        else:
            self.status=EINGEFAHREN_RECHTS3
        
    def kopfmachenRechts3(self):
        # überfahren lassen
        time.sleep(2.5)
        self.stop()
        print "BR 110 Abkuppeln auf Gleis 3 (rechts)"
        # anrücken
        time.sleep(1)
        self.direction(0)
        self.speed(1)
        time.sleep(1)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.direction(1)
        entkuppler3.actuate(0, 1,0)
        time.sleep(1)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.speed(40)
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)        
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)
        entkuppler3.actuate(0, 1, 0)
        time.sleep(0.1)
        time.sleep(3)  
        self.stop()
        time.sleep(2)      
        weiche34.actuate(1, 1)
        time.sleep(1)
        einfahrt4()
        time.sleep(2)
        self.direction(0)
        self.speed(50)
            
    def kopfmachenLinks(self):
        time.sleep(1.4)
        self.stop()
        print "BR 110 Abkuppeln auf Gleis 1 (links)"

        #anrücken:
        time.sleep(1)
        self.direction(RECHTS)
        time.sleep(1)        
        self.speed(40)
        time.sleep(0.5)        
        entkupplenLinks(2)
        self.stop()
        time.sleep(0.5)
        self.direction(0)
        entkupplenLinks(2)        
        self.speed(40)
        entkupplenLinks(2)
        time.sleep(4)
        self.stop()
        time.sleep(1)        
        weiche10.actuate(0, 1)
        time.sleep(1)        
        weiche10.actuate(0, 1)
        time.sleep(1)        
        self.direction(1)
        time.sleep(1)
        self.speed(60)

    def von1nachRechts3(self,delay):
        print "BR 110 startet nach rechts 3 in",delay,"sekunden"
        time.sleep(delay)
        bahnhofLinksGerade()        
        self.direction(1)
        time.sleep(3)
        self.speed(128)
        time.sleep(28)
        einfahrt3()
        
    def von3nachLinks1(self,delay=1):
        print "BR 110 nach links in",delay,"sekunden"
        time.sleep(delay)
        ausfahrt3()
        self.direction(0)
        time.sleep(1)
        self.speed(70)
        time.sleep(16)
        self.speed(128)
        time.sleep(6)
        bahnhofLinksGerade()
        self.status=EINFAHRT_LINKS1
        
    def startEntkuppelnLinks(self,delay=1):
        print "BR 110 Abkuppeln links"
        time.sleep(delay)
        weiche10.actuate(1, 1)
        time.sleep(1)
        self.direction(LINKS)
        time.sleep(1)        
        self.status=KOPFMACHEN_LINKS
        self.speed(41)

    def startEntkuppelnRechts(self,delay):
        print "BR 110 Abkuppeln rechts"
        time.sleep(delay)
        self.status=KOPFMACHEN_RECHTS3  
        self.direction(1)
        time.sleep(0.5)        
        self.speed(30)
        
# EVENTS
        
    def entkupplerLinksEvent(self):
        print "Entkupplerkontakt links"
        if (self.status==KOPFMACHEN_LINKS):
            self.kopfmachenLinks()  
        else:
            time.sleep(1)
    
    def entkupplerRechts3Event(self):
        print "Entkupplerkontakt rechts (3)"
        if (self.status==KOPFMACHEN_RECHTS3):
            self.kopfmachenRechts3()     
        else:
            time.sleep(1)
            
    def einfahrtLinksEvent(self):
        print "Einfahrtkontakt links"
        if (self.status==EINFAHRT_LINKS1):
            self.einfahrtLinks()
        elif (self.status==KOPFMACHEN_LINKS):
            self.stop()
            time.sleep(1)
            self.ankuppeln1()
        else:
            time.sleep(1)

    def einfahrtRechtsEvent(self):
        print "Einfahrtkontakt rechts"
        if (self.status==KOPFMACHEN_RECHTS3):
            self.stop()
            time.sleep(2)
            weiche34.actuate(0, 1)
            self.ankuppeln3()
        elif (self.status==NACH_RECHTS3):
            self.einfahrtRechts3()
        else:
            time.sleep(1)

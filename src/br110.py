# coding=utf8
from lok import *
import time,os,srcp
from weichen import ausfahrt3, weiche10, entkupplenLinks,\
    bahnhofLinksGerade, einfahrt3, entkuppler3, weiche34, einfahrt4

class BR110(Lok):
        
    def ankuppeln1(self):
        print "Ankuppeln auf Gleis 1 (links)"
        self.status=ANKUPPELN        
        self.direction(LINKS)
        time.sleep(1)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(60)
        time.sleep(9)
        self.speed(20)
        time.sleep(11)
        self.stop()
        self.status=BEREIT_LINKS1
        
    def ankuppeln3(self):
        print "Ankuppeln auf Gleis 3 (rechts)"
        time.sleep(1)
        einfahrt3()
        time.sleep(2)
        self.direction(1)
        time.sleep(2)
        self.speed(60)
        time.sleep(15)
        self.stop()
        self.status=BEREIT_RECHTS3
        
    def kopfmachenRechts3(self):
        # überfahren lassen
        time.sleep(2)
        self.stop()
        print "Abkuppeln auf Gleis 3 (rechts)"
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
        time.sleep(1.5)
        self.stop()
        print "Abkuppeln auf Gleis 1 (links)"

        #anrücken:
        time.sleep(1)
        self.direction(RECHTS)
        time.sleep(0.6)        
        self.speed(40)
        time.sleep(0.65)        
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
        print "BR110 startet nach rechts 3 in",delay,"sekunden"
        time.sleep(delay)        
        self.direction(1)
        time.sleep(3)
        self.speed(128)
        time.sleep(28)
        einfahrt3()
        
    def von3nachLinks1(self,delay=1):
        print "BR 110 nach links in",delay,"sekunden"
        time.sleep(delay)
        ausfahrt3()
        bahnhofLinksGerade()
        self.direction(0)
        time.sleep(1)
        self.speed(61)
        time.sleep(19)
        self.speed(128)
        time.sleep(6)
        self.status=self.EINFAHRT_LINKS1
        
    def startEntkuppelnLinks(self,delay=1):
        print "Abkuppeln links"
        time.sleep(delay)
        weiche10.actuate(1, 1)
        time.sleep(1)
        self.direction(LINKS)
        time.sleep(1)        
        self.status=KOPFMACHEN_LINKS
        self.speed(35)        

    def startEntkuppelnRechts(self,delay):
        print "Abkuppeln rechts"
        time.sleep(delay)
        self.status=KUPPLUNG_AKTIV  
        self.direction(1)
        time.sleep(0.5)        
        self.speed(30)
        
# EVENTS
        
    def entkupplerLinksEvent(self):
        if (self.status==KOPFMACHEN_LINKS):
            self.kopfmachenLinks()  
    
    def entkupplerRechts3Event(self):
        if (self.status==KUPPLUNG_AKTIV):
            self.kopfmachenRechts3()     
            
    def einfahrtLinksEvent(self):
        if (self.status==EINFAHRT_LINKS1):
            self.stop()
            self.notbremse()
        elif (self.status==KOPFMACHEN_LINKS):
            self.stop()
            time.sleep(1)
            self.ankuppeln1()

    def einfahrtRechtsEvent(self):
        if (self.status==KUPPLUNG_AKTIV):
            self.stop()
            time.sleep(2)
            weiche34.actuate(0, 1)
            self.ankuppeln3()
        elif (self.status==NACH_RECHTS3):
            print "brake..."
            self.speed(40)
            time.sleep(24)
            self.stop()
            time.sleep(1)
            self.status=EINGEFAHREN_RECHTS3

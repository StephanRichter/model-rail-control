# coding=utf8
from lok import *
import time,os,srcp
from weichen import ausfahrt3, weiche10, entkupplenLinks,\
    bahnhofLinksGerade, einfahrt3, entkuppler3, weiche34, einfahrt4

class BR110(Lok):
        
    def ankuppeln3(self):
        time.sleep(1)
        einfahrt3()
        time.sleep(2)
        self.direction(1)
        time.sleep(2)
        self.speed(60)
        time.sleep(15)
        self.stop()
        self.status=Lok.BEREIT_RECHTS3
    
    def kopfmachenRechts3(self):
        # überfahren lassen
        time.sleep(2)
        self.stop()
        # anrücken
        time.sleep(1)
        self.direction(0)
        self.speed(1)
        time.sleep(0.7)        
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
        self.status=self.KRITISCHE_PHASE
        self.status=0
        self.stop()
        #anrücken:
        time.sleep(1)
        self.direction(1)
        time.sleep(0.5)        
        self.speed(40)
        time.sleep(0.62)        
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
        weiche10.actuate(0, 1)
        time.sleep(0.2)        
        weiche10.actuate(0, 1)
        time.sleep(1)
        self.direction(1)
        time.sleep(1)
        self.speed(60)
        time.sleep(25)
        self.stop()
        bahnhofLinksGerade()
        self.direction(0)
        time.sleep(1)
        self.speed(60)
        time.sleep(10)
        self.speed(20)
        time.sleep(10)
        self.stop()
        self.status=self.BEREIT_LINKS1

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
        self.direction(0)
        time.sleep(1)
        ausfahrt3()
        time.sleep(1)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(60)
        time.sleep(20)
        self.speed(128)
        time.sleep(37)
        self.stop()
        self.status=self.EINGEFAHREN_LINKS1
        
    def startEntkuppelnLinks(self,delay=1):
        time.sleep(delay)
        self.direction(0)
        time.sleep(1)        
        self.status=self.KOPFMACHEN_LINKS
        self.speed(40)        
            
    def action16(self):
        if (self.status==self.KOPFMACHEN_LINKS):
            self.kopfmachenLinks()
        else:     
            self.stop()
            os._exit(0)
    
    def action32(self):
        if (self.status==Lok.KUPPLUNG_AKTIV):
            self.kopfmachenRechts3()     
        else:
            os._exit(0)
    
    def action64(self):
        if (self.status==Lok.KUPPLUNG_AKTIV):
            self.stop()
            time.sleep(2)
            weiche34.actuate(0, 1)
            self.ankuppeln3()
        elif (self.status==Lok.NACH_RECHTS3):
            print "brake..."
            self.speed(40)
            time.sleep(24)
            self.stop()
            time.sleep(1)
            self.status=Lok.EINGEFAHREN_RECHTS3
                
    def startEntkuppelnRechts(self,delay):
        time.sleep(delay)
        self.status=Lok.KUPPLUNG_AKTIV  
        self.direction(1)
        time.sleep(0.5)        
        self.speed(30)
        

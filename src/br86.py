# coding=utf8
from lok import *
import time,os,srcp
from weichen import *

class BR86(Lok):
    name = "BR 86 "
    def ankuppeln1(self):
        print "BR 86 Ankuppeln auf Gleis 1 (links)"
        self.status=ANKUPPELN        
        self.direction(LINKS)
        time.sleep(1)
        bahnhofLinksGerade()
        time.sleep(1)
        self.speed(20)
        time.sleep(19)
        self.stop()
        self.status=BEREIT_LINKS1
        
    def ankuppeln2(self):
        print "BR 86 Ankuppeln auf Gleis 2 (rechts)"
        time.sleep(1)
        einfahrt2()
        time.sleep(2)
        self.direction(RECHTS)
        time.sleep(2)
        self.speed(60)
        time.sleep(5)
        self.speed(20)
        time.sleep(2)
        self.speed(5)
        time.sleep(20)
        self.stop()
        self.status=BEREIT_RECHTS2
        
    def ankuppeln3(self):
        print "BR 86 Ankuppeln auf Gleis 3 (rechts)"
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
        print "BR 86 fährt auf Gleis 1 (links) ein"
        self.speed(100)
        time.sleep(3)
        self.speed(80)
        time.sleep(2)
        self.speed(60)
        time.sleep(2)
        self.speed(40)
        time.sleep(6)
        self.speed(20)
        time.sleep(6)
        self.stop()
        self.status=EINGEFAHREN_LINKS1
        
    def einfahrtRechts2(self):
        print "BR 86 fährt auf Gleis 2 (rechts) ein"
        self.status=EINFAHRT_RECHTS2
        self.speed(80)            
        time.sleep(2)
        self.speed(60)
        time.sleep(4)
        self.speed(40)
        time.sleep(5)
        self.speed(20)

    def einfahrtRechts3(self):
        print "BR 86 fährt auf Gleis 3 (rechts) ein"
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
        self.status=EINGEFAHREN_RECHTS3
        
    def kopfmachenLinks(self):
        time.sleep(3)
        self.stop()
        print "Abkuppeln auf Gleis 1 (links)"

        #anrücken:
        time.sleep(1)
        self.direction(RECHTS)
        time.sleep(1)        
        self.speed(40)
        time.sleep(0.4)        
        entkupplenLinks(2)
        self.stop()
        time.sleep(0.5)
        self.direction(LINKS)
        entkupplenLinks(2)        
        self.speed(40)
        entkupplenLinks(2)
        time.sleep(3.5)
        self.stop()
        time.sleep(1)        
        weiche10.actuate(0, 1)
        time.sleep(1)        
        weiche10.actuate(0, 1)
        time.sleep(1)        
        self.direction(RECHTS)
        time.sleep(1)
        self.speed(60)

    def kopfmachenRechts2(self):
        # anrücken
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        self.direction(RECHTS)
        entkuppler2.actuate(1, 1,0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1,0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1,0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        self.speed(20)
        entkuppler2.actuate(1, 1,0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1,0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(0.2)        
        entkuppler2.actuate(1, 1, 0)
        time.sleep(4)
        self.stop()
        time.sleep(1)      
        einfahrt1()
        time.sleep(1)
        weiche12.actuate(1, 1)
        time.sleep(1)
        self.direction(LINKS)
        self.speed(70)
            
    def kopfmachenRechts3(self):
        # überfahren lassen
        time.sleep(2.5)
        self.stop()
        print "Abkuppeln auf Gleis 3 (rechts)"
        # anrücken
        time.sleep(1)
        self.direction(LINKS)
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
        weiche12.actuate(1, 1)
        time.sleep(1)
        einfahrt4()
        time.sleep(2)
        self.direction(0)
        self.speed(50)
            
    def von1nachLinks1(self,delay=1):
        print "BR 86 nach links in",delay,"sekunden"
        time.sleep(delay)
        self.lichtAn()
        time.sleep(1)        
        ausfahrt1()
        self.direction(0)
        time.sleep(1)
        self.speed(70)
        time.sleep(16)
        self.speed(128)
        time.sleep(6)
        bahnhofLinksGerade()
        self.status=EINFAHRT_LINKS1

    def von1nachRechts2(self,delay):
        print "BR 86 startet nach rechts 2 in",delay,"sekunden"
        time.sleep(delay)
        self.direction(RECHTS)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)        
        bahnhofLinksGerade()        
        time.sleep(1)
        self.speed(128)
        time.sleep(20)
        einfahrt2()

    def von1nachRechts3(self,delay):
        print "BR110 startet nach rechts 3 in",delay,"sekunden"
        time.sleep(delay)
        self.lichtAn()
        time.sleep(1)        
        bahnhofLinksGerade()        
        self.direction(1)
        time.sleep(3)
        self.speed(128)
        time.sleep(28)
        einfahrt3()
        
    def von2nachLinks1(self,delay=1):
        print "BR 86 nach links in",delay,"sekunden"
        time.sleep(delay)
        self.lichtAn()
        time.sleep(1)        
        ausfahrt2()
        self.direction(0)
        time.sleep(1)
        self.speed(70)
        time.sleep(16)
        self.speed(128)
        time.sleep(6)
        bahnhofLinksGerade()
        self.status=EINFAHRT_LINKS1        
        
    def von3nachLinks1(self,delay=1):
        print "BR 86 nach links in",delay,"sekunden"
        time.sleep(delay)
        self.lichtAn()
        time.sleep(1)        
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
        print "Abkuppeln links"
        time.sleep(delay)
        weiche10.actuate(1, 1)
        time.sleep(1)
        self.direction(LINKS)
        time.sleep(1)        
        self.status=KOPFMACHEN_LINKS
        self.speed(41)

    def startEntkuppelnRechts2(self,delay):
        print "BR 86 Abkuppeln rechts Gleis (2)"
        time.sleep(delay)
        self.status=KOPFMACHEN_RECHTS2
        weiche12.actuate(0, 1)
        time.sleep(0.5)  
        self.direction(LINKS)
        time.sleep(0.5)        
        self.speed(20)

    def startEntkuppelnRechts3(self,delay):
        print "BR 86 Abkuppeln rechts Gleis (2)"
        time.sleep(delay)
        self.status=KOPFMACHEN_RECHTS3  
        self.direction(1)
        time.sleep(0.5)        
        self.speed(30)
        
    def startWechsel2(self,delay):
        print "BR 86 wechselt von Gleis 2 in",delay,"sekunden"
        time.sleep(delay)
        self.direction(LINKS)
        einfahrt2()
        self.lichtAn()
        time.sleep(1)
        self.speed(40)
        
    def startWechsel3(self,delay):
        print "BR 86 wechselt von Gleis 3 in",delay,"sekunden"
        time.sleep(delay)
        self.direction(LINKS)
        einfahrt3()
        self.lichtAn()
        time.sleep(1)
        self.speed(40)

    def wechselNach1(self):
        time.sleep(15)
        self.stop()
        self.status=WECHSEL_NACH_1
        time.sleep(2)
        einfahrt1()
        time.sleep(1)
        self.direction(RECHTS)
        time.sleep(1)
        self.speed(40)
        
    def wechselNach3(self):
        time.sleep(15)
        self.stop()
        self.status=WECHSEL_NACH_3
        time.sleep(2)
        einfahrt3()
        time.sleep(1)
        self.direction(RECHTS)
        time.sleep(1)
        self.speed(40)
        
# EVENTS
        
    def entkupplerLinksEvent(self):
        if (self.status==KOPFMACHEN_LINKS):
            self.kopfmachenLinks()  
    
    def entkupplerRechts2Event(self):
        if (self.status==KOPFMACHEN_RECHTS2):
            self.kopfmachenRechts2()
        elif (self.status==EINFAHRT_RECHTS2):
            self.stop()
            self.status=EINGEFAHREN_RECHTS2          

    def entkupplerRechts3Event(self):
        if (self.status==KOPFMACHEN_RECHTS3):
            self.kopfmachenRechts3()     
            
    def einfahrtLinksEvent(self):
        if (self.status==EINFAHRT_LINKS1):
            self.einfahrtLinks()
        elif (self.status==KOPFMACHEN_LINKS):
            self.stop()
            time.sleep(1)
            self.ankuppeln1()
        elif (self.status==KOPFMACHEN_RECHTS2):
            self.notbremse()

    def einfahrtRechtsEvent(self):
        if (self.status==KOPFMACHEN_RECHTS2):
            self.stop()
            self.ankuppeln2()
        elif (self.status==KOPFMACHEN_RECHTS3):
            self.stop()
            time.sleep(2)
            weiche34.actuate(0, 1)
            self.ankuppeln3()
        elif (self.status==NACH_RECHTS2):
            self.einfahrtRechts2()
        elif (self.status==NACH_RECHTS3):
            self.einfahrtRechts3()
        elif (self.status==WECHSEL_NACH_1):
            time.sleep(10)
            self.stop()
            self.status=BEREIT_RECHTS1
        elif (self.status==WECHSEL_NACH_3):
            time.sleep(11)
            self.stop()
            self.status=BEREIT_RECHTS3
        elif (self.status==WECHSEL_2_NACH_3):
            self.wechselNach3()
        elif (self.status==WECHSEL_3_NACH_1):
            self.wechselNach1()

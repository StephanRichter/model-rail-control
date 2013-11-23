# coding=utf8
from thread import allocate_lock
import time
import srcp
from kontakte import *
from weichen import *

UNDEFINED=-1

# status:
NACH_LINKS=0
NACH_RECHTS=1

ABGEKUPPELT=13
ABKUPPELN=2
ANKUPPELN=3
AUSFAHRT=4
BEREIT=5
EINFAHRT=6
EINGEFAHREN=7
UMFAHREN=8
GLEISWECHSEL=9

PARKED=12

# Bahnhof
LINKS=10
RECHTS=11

WENDEZEIT=1

class Lok:
    
    name = "unbekannte Lok"    
    status=UNDEFINED
    vonGleis=UNDEFINED
    nachGleis=UNDEFINED
    bahnhof=UNDEFINED
    wendezug=False
    zuglaenge=40    
    
    def __init__(self,lok):
        self.lok=lok
        lok.init('N', '1', 128, 4) # Protokoll, Version, Fahrstufen, Funktionen
        
# <===== Events / Kontakte ===================

    def action(self,contact):
        if (contact == KONTAKT_EINFAHRT_RECHTS):
            self.fireEinfahrtRechtsEvent()
        elif (contact == KONTAKT_EINFAHRT_LINKS):
            self.fireEinfahrtLinksEvent()
        elif (contact == KONTAKT_ENTKUPPLER_LINKS):
            self.fireEntkupplerLinksEvent()
        elif (contact == KONTAKT_ENTKUPPLER_RECHTS2):
            self.fireEntkupplerRechts2Event()
        elif (contact == KONTAKT_ENTKUPPLER_RECHTS3):
            self.fireEntkupplerRechts3Event()
        else:
            print "contact",contact
            
    einfahrtRechtsLock = allocate_lock()
    einfahrtRechtsActive = False
    
    def einfahrtRechtsEvent(self):
        print "Einfahrtkontakt rechts ausgelöst"
        time.sleep(5)


    def fireEinfahrtRechtsEvent(self):
        self.einfahrtRechtsLock.acquire()
        if (self.einfahrtRechtsActive):
            self.einfahrtRechtsLock.release();
            return
        self.einfahrtRechtsActive = True
        self.einfahrtRechtsLock.release();
        self.einfahrtRechtsEvent()
        print "Einfahrtkontakt rechts"
        self.einfahrtRechtsLock.acquire()
        self.einfahrtRechtsActive = False
        self.einfahrtRechtsLock.release();
        
    einfahrtLinksLock = allocate_lock()
    einfahrtLinksActive = False             
            
    def einfahrtLinksEvent(self):
        print "Einfahrtkontakt Links ausgelöst"
        time.sleep(5)


    def fireEinfahrtLinksEvent(self):
        self.einfahrtLinksLock.acquire()
        if (self.einfahrtLinksActive):
            self.einfahrtLinksLock.release();
            return
        self.einfahrtLinksActive = True
        self.einfahrtLinksLock.release();
        self.einfahrtLinksEvent()
        self.einfahrtLinksLock.acquire()
        self.einfahrtLinksActive = False
        self.einfahrtLinksLock.release();

    entkupplerLinksLock = allocate_lock()
    entkupplerLinksActive = False             
            
    def entkupplerLinksEvent(self):
        print "Entkupplerkontakt Links ausgelöst"
        time.sleep(5)

    def fireEntkupplerLinksEvent(self):
        self.entkupplerLinksLock.acquire()
        if (self.entkupplerLinksActive):
            self.entkupplerLinksLock.release();
            return
        self.entkupplerLinksActive = True
        self.entkupplerLinksLock.release();
        self.entkupplerLinksEvent()
        self.entkupplerLinksLock.acquire()
        self.entkupplerLinksActive = False
        self.entkupplerLinksLock.release();
        
    entkupplerRechts2Lock = allocate_lock()
    entkupplerRechts2Active = False             
            
    def entkupplerRechts2Event(self):
        print "Entkupplerkontakt Rechts2 ausgelöst"
        time.sleep(5)

    def fireEntkupplerRechts2Event(self):
        self.entkupplerRechts2Lock.acquire()
        if (self.entkupplerRechts2Active):
            self.entkupplerRechts2Lock.release();
            return
        self.entkupplerRechts2Active = True
        self.entkupplerRechts2Lock.release();
        self.entkupplerRechts2Event()
        self.entkupplerRechts2Lock.acquire()
        self.entkupplerRechts2Active = False
        self.entkupplerRechts2Lock.release();     
        
    entkupplerRechts3Lock = allocate_lock()
    entkupplerRechts3Active = False             
            
    def entkupplerRechts3Event(self):
        print "Entkupplerkontakt Rechts3 ausgelöst"
        time.sleep(5)

    def fireEntkupplerRechts3Event(self):
        self.entkupplerRechts3Lock.acquire()
        if (self.entkupplerRechts3Active):
            self.entkupplerRechts3Lock.release();
            return
        self.entkupplerRechts3Active = True
        self.entkupplerRechts3Lock.release();
        self.entkupplerRechts3Event()
        self.entkupplerRechts3Lock.acquire()
        self.entkupplerRechts3Active = False
        self.entkupplerRechts3Lock.release();
        
# =========== Events / Kontakte ===========>

    def sleep(self,secs):
        time.sleep(secs)

# <========== Aktionen =====================
    def lichtAn(self):
        self.lok.setF(0,1)
        self.lok.send()
        
    def lichtAus(self):
        self.lok.setF(0,0)
        self.lok.send()
        
    def nachLinks(self):
        self.lok.setDirection(0)
        self.lok.send()
        
    def nachRechts(self):
        self.lok.setDirection(1)
        self.lok.send()
        
    def speed(self,speed):
        self.lok.setSpeed(speed)
        self.lok.send()
        
    def stop(self):
        self.lok.setSpeed(0)
        self.lok.send()
        time.sleep(0.1)
        self.lok.setSpeed(0)
        self.lok.send()
        time.sleep(0.1)
        self.lok.setSpeed(0)
        self.lok.send()
               
    def notbremse(self):
        self.stop()
        self.status=0
        
    def abkuppeln(self,delay=3):
        if (self.bahnhof==LINKS):
            self.abkuppelnLinks(delay)
        elif (self.bahnhof==RECHTS):
            self.abkuppelnRechts(delay)

        else:
            print "kann nicht abkuppeln, da nicht bekannt ist, wo sich",self.name," befindet"
            
    def abkuppelnLinks(self,delay=3):
        self.notImplemented("abkuppelnLinks")

    def abkuppelnRechts(self,delay=3):
        if (self.vonGleis==3):
            self.abkuppelnRechts3(delay)
        else:
            print "rechts gibt es kein Gleis",self.vonGleis
            
    def abkuppelnRechts3(self,delay=3):
        self.notImplemented("abkuppelnRechts3")


    def ankuppeln(self,delay=3):
        if (self.bahnhof==LINKS):
            self.ankuppelnLinks(delay)
        else:
            print "kann nicht ankuppeln, da nicht bekannt ist, wo sich",self.name," befindet"
        
    def ankuppelnLinks(self,delay=3):
        print self.name,"kuppelt in",delay,"Sekunden an"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksGerade()
        time.sleep(0.1)
        self.speed(30)
        
    def ankuppelnRechts(self,delay=3):
        print self.name,"kuppelt in",delay,"Sekunden an"
        self.nachRechts()
        self.lichtAn()
        time.sleep(delay)
        self.einfahrWeichenRechts()        
        time.sleep(0.1)
        self.speed(30)

    def ausfahrt(self,delay=3):
        if (self.bahnhof==LINKS):
            self.ausfahrtLinks(delay)
        else:
            print "kann nicht ausfahren, da nicht bekannt ist, wo sich",self.name," befindet"
        
    def ausfahrtLinks(self,delay=3):        
        print self.name," fährt aus Bahnhof links aus in",delay,"sekunden"
        self.nachRechts()
        self.lichtAn()
        time.sleep(delay)
        if (self.vonGleis==1):
            bahnhofLinksGerade()
        elif (self.vonGleis==2):
            bahnhofLinksAbzweig()
        else:
            print "links gibt es kein Gleis",self.vonGleis
            return
        self.speed(50)
        
    def ausfahrtRechts(self,delay=3):
        if (self.bahnhof!=RECHTS):
            print self.name," ist nicht rechts, kann auch dort nicht ausfahren"
            return
        print self.name," fährt aus Bahnhof rechts aus in",delay,"sekunden"
        self.status=NACH_LINKS
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        if (self.vonGleis==1):
            ausfahrt1()
        elif (self.vonGleis==2):
            ausfahrt2()
        elif (self.vonGleis==3):
            ausfahrt3()
        elif (self.vonGleis==4):
            ausfahrt4()
        else:
            print "rechts gibt es kein Gleis",self.vonGleis
            return
        self.speed(50)
        
    def einfahrt(self,delay=3):
        if (self.status==NACH_RECHTS):
            self.einfahrtRechts(delay)
            self.bahnhof=RECHTS
        else:
            print "kann nicht einfahren, da nicht bekannt ist, wo",self.name,"hinfährt"
            
    def einfahrWeichenRechts(self):       
        if (self.nachGleis==1):
            einfahrt1()
        elif (self.nachGleis==2):
            einfahrt2()
        elif (self.nachGleis==3):
            einfahrt3()
        elif (self.nachGleis==4):
            einfahrt4()
        else:
            self.stop()
            print "rechts gibt es kein Gleis",self.nachGleis
            return
            
    def einfahrtRechts(self):
        self.einfahrWeichenRechts()
        self.status=EINFAHRT
        
    def eingefahren(self):
            self.stop()
            time.sleep(3)
            self.lichtAus()
            self.vonGleis=self.nachGleis
            self.nachGleis=UNDEFINED
            self.status=EINGEFAHREN
        
    def notImplemented(self,name):
        print name," nicht implementiert für",self.name
        
    def stat(self,status,bahnhof=UNDEFINED,vonGleis=UNDEFINED):
        return (status==self.status) & (bahnhof==self.bahnhof) & (vonGleis==self.vonGleis)
    
    def umfahren(self,delay=3):
        if (self.bahnhof==LINKS):
            self.umfahrenLinks(delay)
        elif (self.bahnhof==RECHTS):
            self.umfahrenRechts(delay)
        else:            
            print "kann nicht umfahren, da nicht bekannt ist, wo sich",self.name,"befindet"
            
    def umfahrenLinks(self,delay=3):
        print self.name,"umfährt in",delay,"Sekunden"
        self.nachRechts()
        self.lichtAn()
        time.sleep(delay)
        bahnhofLinksAbzweig()
        self.speed(40)
        
    def umfahrenRechts(self,delay=3):
        print self.name,"umfährt in",delay,"Sekunden"
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        if (self.vonGleis==3):
            self.vonGleis=4
            self.nachGleis=4 # für self.einfahrtRechts
            self.einfahrWeichenRechts()
            self.nachGleis=3
            weiche34.actuate(1, 1)
            time.sleep(1)
        else:
            print "keine Aktion definiert für Lok auf Gleis",self.vonGleis
            self.status=UNDEFINED
            self.sleep(10)
        self.speed(40)

# ============= Aktionen =================>               

    def state(self):
        print self.name,":"
        if (self.bahnhof == LINKS):
            print " Bahnhof LINKS, "
        if (self.bahnhof == RECHTS):
            print " Bahnhof RECHTS, "

        if (self.status == UNDEFINED):
            print "UNDEFINED"
        elif (self.status == ABKUPPELN):
            print "ABKUPPELN"
        elif (self.status == ANKUPPELN):
            print "ANKUPPELN"
        elif (self.status == AUSFAHRT):
            print "AUSFAHRT"
        elif (self.status == BEREIT):
            print "BEREIT"
        elif (self.status == EINFAHRT):
            print "EINFAHRT"
        elif (self.status == EINGEFAHREN):
            print "EINGEFAHREN"
        elif (self.status == NACH_LINKS):
            print "NACH_LINKS"
        elif (self.status == NACH_RECHTS):
            print "NACH_RECHTS"
        elif (self.status == UMFAHREN):
            print "UMFAHREN"
        elif (self.status == GLEISWECHSEL):
            print "GLEISWECHSEL"
        elif (self.status == PARKED):
            print "PARKED"
        elif (self.status == ABGEKUPPELT):
            print "ABGEKUPPELT"
        else:
            print "unknown:",self.status
            
        print self.vonGleis,"=>",self.nachGleis

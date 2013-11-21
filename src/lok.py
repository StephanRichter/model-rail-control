# coding=utf8
from thread import allocate_lock
import time
import srcp
from kontakte import *

UNDEFINED=0

# status:
ABKUPPELN=1
ANKUPPELN=2
AUSFAHRT=3
BEREIT=4
EINFAHRT=5
EINGEFAHREN=6
NACH_LINKS=7
NACH_RECHTS=8
UMFAHREN=9
GLEISWECHSEL=10

# Bahnhof
LINKS=11
RECHTS=12

class Lok:
    
    name = "unbekannte Lok"    
    status=UNDEFINED
    vonGleis=UNDEFINED
    nachGleis=UNDEFINED
    bahnhof=UNDEFINED    
    
    def __init__(self,lok):
        self.lok=lok
        lok.init('N', '1', 128, 4)
        
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
        
    def lichtAn(self):
        self.lok.setF(0,1)
        self.lok.send()
        
    def lichtAus(self):
        self.lok.setF(0,0)
        self.lok.send()
        
    def direction(self,dir):
        self.lok.setDirection(dir)        
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
        else:
            print "unknown:",self.status
            
        print self.vonGleis,"=>",self.nachGleis

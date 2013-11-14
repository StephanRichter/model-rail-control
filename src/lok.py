# coding=utf8
from thread import allocate_lock
import time
import srcp
from kontakte import *

UNDEFINED=0
ANKUPPELN=1
BEREIT_LINKS1=2
BEREIT_RECHTS1=3
BEREIT_RECHTS3=4
BEREIT_RECHTS4=5
EINFAHRT_LINKS1=6
EINFAHRT_RECHTS3=7
EINFAHRT_RECHTS4=8
EINGEFAHREN_LINKS1=9
EINGEFAHREN_RECHTS3=10
KOPFMACHEN_LINKS=11
KOPFMACHEN_RECHTS3=12
KRITISCHE_PHASE=666
NACH_RECHTS3=13
NACH_LINKS1=14
NACH_LINKS2=15
NACH_RECHTS4=16
EINFAHRT_LINKS2=17
BEREIT_LINKS2=18
NACH_RECHTS2=19
BEREIT_RECHTS2=20
EINGEFAHREN_RECHTS2=21
KOPFMACHEN_RECHTS2=22
NACH_RECHTS1=23
EINFAHRT_RECHTS1=24
    
RECHTS=1
LINKS=0

class Lok:
    
    name = "unbekannte Lok"    
    status=0    
    
    def __init__(self,lok):
        self.lok=lok
        lok.init('N', '1', 128, 4)

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
    
    def notbremse(self):
        self.stop()
        self.status=0               
            
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

    def state(self):
        if (self.status == UNDEFINED):
            print self.name,": UNDEFINED"
        elif (self.status == ANKUPPELN):
            print self.name,": ANKUPPELN"
        elif (self.status == BEREIT_LINKS1):
            print self.name,": BEREIT_LINKS1"
        elif (self.status == BEREIT_RECHTS1):
            print self.name,": BEREIT_RECHTS1"
        elif (self.status == BEREIT_RECHTS3):
            print self.name,": BEREIT_RECHTS3"
        elif (self.status == BEREIT_RECHTS4):
            print self.name,": BEREIT_RECHTS4"
        elif (self.status == EINFAHRT_LINKS1):
            print self.name,": EINFAHRT_LINKS1"
        elif (self.status == EINFAHRT_RECHTS3):
            print self.name,": EINFAHRT_RECHTS3"
        elif (self.status == EINFAHRT_RECHTS4):
            print self.name,": EINFAHRT_RECHTS4"
        elif (self.status == EINGEFAHREN_LINKS1):
            print self.name,": EINGEFAHREN_LINKS1"
        elif (self.status == EINGEFAHREN_RECHTS3):
            print self.name,": EINGEFAHREN_RECHTS3"
        elif (self.status == KOPFMACHEN_LINKS):
            print self.name,": KOPFMACHEN_LINKS"
        elif (self.status == KOPFMACHEN_RECHTS3):
            print self.name,": KOPFMACHEN_RECHTS3"
        elif (self.status == KRITISCHE_PHASE):
            print self.name,": KRITISCHE_PHASE"
        elif (self.status == NACH_RECHTS3):
            print self.name,": NACH_RECHTS3"
        elif (self.status == NACH_LINKS1):
            print self.name,": NACH_LINKS1"
        elif (self.status == NACH_LINKS2):
            print self.name,": NACH_LINKS2"
        elif (self.status == NACH_RECHTS4):
            print self.name,": NACH_RECHTS4"
        elif (self.status == EINFAHRT_LINKS2):
            print self.name,": EINFAHRT_LINKS2"
        elif (self.status == BEREIT_LINKS2):
            print self.name,": BEREIT_LINKS2"
        elif (self.status == NACH_RECHTS2):
            print self.name,": NACH_RECHTS2"
        elif (self.status == BEREIT_RECHTS2):
            print self.name,": BEREIT_RECHTS2"
        elif (self.status == EINGEFAHREN_RECHTS2):
            print self.name,": EINGEFAHREN_RECHTS2"
        elif (self.status == KOPFMACHEN_RECHTS2):
            print self.name,": KOPFMACHEN_RECHTS2"
        elif (self.status == NACH_RECHTS1):
            print self.name,": NACH_RECHTS1"
        elif (self.status == EINFAHRT_RECHTS1):
            print self.name,": EINFAHRT_RECHTS1"
        else:
            print self.name,": unknown:",self.status
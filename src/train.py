# coding=utf8
from thread import allocate_lock
import time
import srcp
from myconsts import *
from environ import *
from switches import *
from thread import start_new_thread
from platf import Platform
from myconsts import *
from multiprocessing.synchronize import Lock

activeTrains=0

class Train:
    
    name = "unbekannte Train"    
    status=UNDEFINED
    targetPlatform=UNDEFINED
    station=UNDEFINED
    platform=UNDEFINED
    pushpull=False
    trainlength=40    
    activeContact=None

    def __init__(self,lok):
        self.lok=lok
        lok.init('N', '1', 128, 4) # Protokoll, Version, Fahrstufen, Funktionen
        
    def __str__(self):
        return self.name
    
# <===== Events / Kontakte ===================
    
    lock = Lock()
    activeContact==None
    
    def contact(self,contact):        
        self.lock.acquire()
        if (self.activeContact==None) and (self.station.hasContact(contact)):
            self.activeContact=contact
            self.lock.release()
            
            if contact==KONTAKT_EINFAHRT_LINKS:
                self.einfahrtLinksEvent()
            elif contact==KONTAKT_EINFAHRT_RECHTS:
                self.einfahrtRechtsEvent()
            elif contact==KONTAKT_ENTKUPPLER_LINKS:
                self.entkupplerLinksEvent()
            elif contact==KONTAKT_ENTKUPPLER_RECHTS2:
                self.entkupplerRechts2Event()
            elif contact==KONTAKT_ENTKUPPLER_RECHTS3:
                self.entkupplerRechts3Event()
            else:
                print "Unknown Contact:",contact
            self.lock.acquire()
            self.activeContact=None
        self.lock.release()        
        
    def einfahrtRechtsEvent(self):
        print "Einfahrtkontakt rechts ausgelöst"
        time.sleep(5)
            
    def einfahrtLinksEvent(self):
        print "Einfahrtkontakt Links ausgelöst"
        time.sleep(5)
            
    def entkupplerLinksEvent(self):
        print "Entkupplerkontakt Links ausgelöst"
        time.sleep(5)
            
    def entkupplerRechts2Event(self):
        print "Entkupplerkontakt Rechts2 ausgelöst"
        time.sleep(5)
            
    def entkupplerRechts3Event(self):
        print "Entkupplerkontakt Rechts3 ausgelöst"
        time.sleep(5)
        
# =========== Events / Kontakte ===========>

    def sleep(self,secs):
        time.sleep(secs)
        
    def possibleTargets(self):
        targs=self.platform.targets
        res=[]
        if self.pushpull:
            for target in targs:
                if self.trainlength<target.length:
                    res.append(target)
        else:
            for target in targs:
                if self.trainlength<target.bypassLength:
                    res.append(target)
        return res
        
# <========== Aktionen =====================
    def lichtAn(self):
        self.lok.setF(0,1)
        self.lok.send()
        self.sleep(0.01)
        
    def lichtAus(self):
        self.lok.setF(0,0)
        self.lok.send()
        
    def direction(self,dir):
        self.lok.setDirection(dir)
        self.lok.send()
        self.sleep(0.01)
        
    def nachLinks(self):
        self.lok.setDirection(0)
        print "<= Fahrtichtung"
        self.lok.send()
        self.sleep(0.02)
        
    def nachRechts(self):
        self.lok.setDirection(1)
        print "Fahrtichtung =>"
        self.lok.send()
        self.sleep(0.02)
        
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
        global l1,r2,r3        
        self.status=ABKUPPELN
        if (self.platform==l1):
            self.abkuppelnLinks(delay)
        elif (self.platform==r2):
            self.abkuppelnRechts2(delay)
        elif (self.platform==r3):
            self.abkuppelnRechts3(delay)

        else:
            print "kann nicht abkuppeln, da nicht bekannt ist, wo sich",self.name," befindet"
            
    def abkuppelnRechts(self,delay=3):
        if (self.vonGleis==2):
            self.abkuppelnRechts2(delay)
        elif (self.vonGleis==3):
            self.abkuppelnRechts3(delay)
        else:
            print "rechts gibt es kein Gleis",self.vonGleis
            
    def abkuppelnRechts2(self,delay=3):
        self.notImplemented("abkuppelnRechts2")

    def abkuppelnRechts3(self,delay=3):
        self.notImplemented("abkuppelnRechts3")

            
    def ankuppeln(self,delay=3):
        print self.name,"kuppelt in",delay,"Sekunden an"
        self.lichtAn()
        time.sleep(delay)
        self.platform.actuateDriveIn()
        time.sleep(0.5)
        self.speed(30)         
    
    def ausfahrt(self,delay=3):
        self.status=AUSFAHRT
        if (self.station==bahnhofLinks):
            self.ausfahrtLinks(delay)
        elif (self.station==bahnhofRechts):
            self.ausfahrtRechts(delay)                    
        else:
            print "kann nicht ausfahren, da nicht bekannt ist, wo sich",self.name," befindet"
        
    def ausfahrtLinks(self,delay=3):        
        print self.name," fährt ausaus in",delay,"sekunden"
        self.nachRechts()
        self.lichtAn()
        time.sleep(delay)
        self.platform.actuateDriveOut()
        time.sleep(1)
        self.speed(50)
        
    def ausfahrtRechts(self,delay=3):
        print self.name,"fährt aus Bahnhof rechts aus in",delay,"sekunden"
        self.status=NACH_LINKS
        self.nachLinks()
        self.lichtAn()
        time.sleep(delay)
        self.platform.actuateDriveOut()
        time.sleep(1)
        self.speed(50)
        
    def einfahrt(self):
        self.platform.setFree()
        self.targetPlatform.actuateDriveIn()
        self.status=EINFAHRT
        self.station=self.targetPlatform.station
            
    def einfahrWeichenLinks(self):
        if (self.nachGleis==1):
            bahnhofLinksGerade()
        elif (self.nachGleis==2):
            bahnhofLinksAbzweig()
        else:
            self.stop()
            print "rechts gibt es kein Gleis",self.nachGleis
            return
        
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

    def eingefahren(self):
            self.stop()
            print self.name,"eingefahren"
            time.sleep(3)
            self.lichtAus()
            if self.pushpull:
                self.setState(self.targetPlatform, BEREIT)
            else:
                self.setState(self.targetPlatform, EINGEFAHREN)
            self.targetPlatform=UNDEFINED
            
    def gleiswechsel(self,delay=3):
        self.status=GLEISWECHSEL
        if (self.bahnhof==RECHTS):
            self.gleiswechselRechts(delay)
        elif (self.bahnhof==LINKS):
            self.gleiswechselLinks(delay)
        else:
            print "Gleiswechsel links nicht definiert"
            
    def gleiswechselLinks(self,delay=3):
        print self.name,"wechselt zu gleis",self.nachGleis,"in",delay,"Sekunden"
        self.nachRechts()
        time.sleep(delay)
        self.lichtAn()
        time.sleep(0.1)
        if (self.vonGleis==1):
            bahnhofLinksGerade()
        else:
            bahnhofLinksAbzweig()
        time.sleep(1)
        self.speed(25)
        
    def gleiswechselRechts(self,delay=3):
        print self.name,"wechselt zu gleis",self.nachGleis,"in",delay,"Sekunden"
        self.nachLinks()
        time.sleep(delay)
        self.lichtAn()
        time.sleep(0.1)
        dummy=self.nachGleis
        self.nachGleis=self.vonGleis
        self.einfahrWeichenRechts()
        time.sleep(1)
        self.nachGleis=dummy
        self.speed(25)
        
    def notImplemented(self,name):
        print name,"nicht implementiert für",self.name
        
    def startAbkuppeln(self,pause):
        start_new_thread(self.abkuppeln,(pause,))

    def startAusfahrt(self,target,pause):
        self.targetPlatform=target
        start_new_thread(self.ausfahrt,(pause,))

    def startGleiswechsel(self,zielgleis,pause):
        self.nachGleis=zielgleis
        start_new_thread(self.gleiswechsel,(pause,))

    def startUmfahren(self,pause):
        start_new_thread(self.umfahren,(pause,))

    def stat(self,status,bahnhof=UNDEFINED,vonGleis=UNDEFINED):
        return (status==self.status) and (bahnhof==self.bahnhof) and (vonGleis==self.vonGleis)
    
    def umfahren(self,delay=3):
        print self.name,"umfährt in",delay,"Sekunden"
        self.status=UMFAHREN
        self.direction(self.platform.bypassDirection)
        self.lichtAn()
        time.sleep(delay)
        self.platform.bypass.actuateDriveIn()
        time.sleep(1)
        self.platform.actuateBypassSwitch()        
        self.speed(40)
            
# ============= Status =================>

    def setState(self,platform,status):        
        platform.setTrain(self)
        self.station=platform.station
        self.platform=platform
        self.status=status

    def state(self):
        txt=self.name+".stat("
        if (self.status == UNDEFINED):
            txt+="UNDEFINED,"
        elif (self.status == ABGEKUPPELT):
            txt+="ABGEKUPPELT,"
        elif (self.status == ABKUPPELN):
            txt+="ABKUPPELN,"
        elif (self.status == ANKUPPELN):
            txt+="ANKUPPELN,"
        elif (self.status == AUSFAHRT):
            txt+="AUSFAHRT,"
        elif (self.status == BEREIT):
            txt+="BEREIT,"
        elif (self.status == EINFAHRT):
            txt+="EINFAHRT,"
        elif (self.status == EINGEFAHREN):
            txt+="EINGEFAHREN,"
        elif (self.status == NACH_LINKS):
            txt+="NACH_LINKS,"
        elif (self.status == NACH_RECHTS):
            txt+="NACH_RECHTS,"
        elif (self.status == UMFAHREN):
            txt+="UMFAHREN,"
        elif (self.status == GLEISWECHSEL):
            txt+="GLEISWECHSEL,"
        elif (self.status == PARKED):
            txt+="PARKED,"
        else:
            txt+="unknown:"+self.status+","            

        if (self.bahnhof == LINKS):
            txt+="LINKS,"
        if (self.bahnhof == RECHTS):
            txt+="RECHTS,"
        print txt+`self.vonGleis`+") => "+`self.nachGleis`

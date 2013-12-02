# coding=utf8
from thread import allocate_lock
import time
import srcp
from kontakte import *
from weichen import *
from thread import start_new_thread
from platf import Platform
from consts import *
from multiprocessing.synchronize import Lock

activeTrains=0

class Train:
    
    name = "unbekannte Lok"    
    status=UNDEFINED
    vonGleis=UNDEFINED
    nachGleis=UNDEFINED
    bahnhof=UNDEFINED
    wendezug=False
    zuglaenge=40    
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

# <========== Aktionen =====================
    def lichtAn(self):
        self.lok.setF(0,1)
        self.lok.send()
        self.sleep(0.01)
        
    def lichtAus(self):
        self.lok.setF(0,0)
        self.lok.send()
        
    def nachLinks(self):
        self.lok.setDirection(0)
        self.lok.send()
        self.sleep(0.01)
        
    def nachRechts(self):
        self.lok.setDirection(1)
        self.lok.send()
        self.sleep(0.01)
        
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
        self.status=ABKUPPELN
        if (self.bahnhof==LINKS):
            self.abkuppelnLinks(delay)
        elif (self.bahnhof==RECHTS):
            self.abkuppelnRechts(delay)

        else:
            print "kann nicht abkuppeln, da nicht bekannt ist, wo sich",self.name," befindet"
            
    def abkuppelnLinks(self,delay=3):
        self.notImplemented("abkuppelnLinks")

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
        if (self.bahnhof==LINKS):
            self.ankuppelnLinks(delay)
        elif (self.bahnhof==RECHTS):
            self.ankuppelnRechts(delay)
        
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
        time.sleep(1)
        self.lichtAn()
        time.sleep(delay)
        self.einfahrWeichenRechts()        
        time.sleep(0.5)
        self.speed(30)

    def ausfahrt(self,delay=3):
        self.status=AUSFAHRT
        if (self.bahnhof==LINKS):
            self.ausfahrtLinks(delay)
        elif (self.bahnhof==RECHTS):
            self.ausfahrtRechts(delay)                    
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
        time.sleep(1)
        self.speed(50)
        
    def ausfahrtRechts(self,delay=3):
        if (self.bahnhof!=RECHTS):
            print self.name,"ist nicht rechts, kann auch dort nicht ausfahren"
            return
        print self.name,"fährt aus Bahnhof rechts aus in",delay,"sekunden"
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
        time.sleep(1)
        self.speed(50)
        
    def einfahrt(self):
        if (self.status==NACH_RECHTS):
            self.einfahrtRechts()
        elif (self.status==NACH_LINKS):
            self.einfahrtLinks()
        else:
            print "kann nicht einfahren, da nicht bekannt ist, wo",self.name,"hinfährt"
            
            
    def einfahrtRechts(self):
        self.einfahrWeichenRechts()
        self.status=EINFAHRT
        self.bahnhof=RECHTS
        
    def einfahrtLinks(self):
        self.einfahrWeichenLinks()
        self.status=EINFAHRT
        self.bahnhof=LINKS

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
            self.vonGleis=self.nachGleis
            self.nachGleis=UNDEFINED
            self.status=EINGEFAHREN
            
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

    def startAusfahrt(self,zielgleis,pause):
        self.nachGleis=zielgleis
        start_new_thread(self.ausfahrt,(pause,))

    def startGleiswechsel(self,zielgleis,pause):
        self.nachGleis=zielgleis
        start_new_thread(self.gleiswechsel,(pause,))

    def startUmfahren(self,pause):
        start_new_thread(self.umfahren,(pause,))

    def stat(self,status,bahnhof=UNDEFINED,vonGleis=UNDEFINED):
        return (status==self.status) and (bahnhof==self.bahnhof) and (vonGleis==self.vonGleis)
    
    def umfahren(self,delay=3):
        self.status=UMFAHREN
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
        if (self.vonGleis==2):
            self.vonGleis=1
            self.nachGleis=1 # für self.einfahrtRechts
            self.einfahrWeichenRechts()
            self.nachGleis=2
            weiche12.actuate(1, 1)
            time.sleep(1)
        elif (self.vonGleis==3):
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

# ============= Status =================>

    def setState(self,platform,status):        
        platform.setTrain(self)
        self.station=platform.station
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
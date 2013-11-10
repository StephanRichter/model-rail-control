from lok import *
import time
from weichen import ausfahrt4, einfahrt4

class ICE(Lok):
    
    def von4nachLinks1(self,delay=1):        
        print "ICE startet nach links 1 in",delay,"sekunden"
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        ausfahrt4()
        time.sleep(1)
        self.speed(50)
        time.sleep(7)
        self.speed(128)
        time.sleep(13)
        self.speed(100)
        time.sleep(1)
        self.speed(80)
        time.sleep(1)
        self.speed(60)
        time.sleep(1)
        self.speed(40)
        time.sleep(2)
        self.speed(20)
        time.sleep(1)
        self.stop()
        self.status=Lok.BEREIT_LINKS1
        
    def von1nachRechts4(self,delay=1):
        print "ICE startet nach rechts 3 in",delay,"sekunden"
        self.direction(1)
        time.sleep(1)
        self.lichtAn()
        time.sleep(1)
        time.sleep(delay-1)
        time.sleep(1)
        self.speed(50)
        time.sleep(8)
        self.speed(128)
        time.sleep(7)
        einfahrt4()
        time.sleep(1)
        self.speed(100)  
    
    def action32(self):
        print "ice 32"
        time.sleep(5)
        
    def action64(self):
        if (self.status==Lok.NACH_RECHTS4):
            time.sleep(1)
            self.speed(80)
            time.sleep(1)
            self.speed(60)
            time.sleep(3)
            self.speed(40)
            time.sleep(2)
            self.speed(20)
            time.sleep(1)
            self.stop()
            self.status=Lok.BEREIT_RECHTS4      


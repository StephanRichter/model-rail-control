from lok import *
import time
from weichen import ausfahrt3

class ICE(Lok):
    
    def von3nachLinks1(self,delay=1):        
        self.direction(0)
        time.sleep(0.5)
        self.lichtAn()
        time.sleep(0.5)
        time.sleep(delay-1)
        print "ICE startet nach links 1"
        ausfahrt3()
        self.direction(0)
        time.sleep(1)
        self.speed(50)
        time.sleep(8)
        self.speed(128)
        time.sleep(10)
        self.speed(100)
        time.sleep(1)
        self.speed(80)
        time.sleep(1)
        self.speed(60)
        time.sleep(1)
        self.speed(40)
        time.sleep(1)
        self.speed(20)
        time.sleep(1)
        self.stop()
        self.status=Lok.BEREIT_LINKS1
    
    def action32(self):
        print "ice 32"
        time.sleep(5)

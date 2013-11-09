from lok import *
import time,os,srcp

class BR110(Lok):
    
    count32 = 0
    entkuppler3=srcp.GA(1,7)
    
    def action32(self):
        self.count32+=1
        if (self.count32== 1):
            time.sleep(2)
            self.stop()
            time.sleep(1)
            self.direction(0)
            self.speed(1)
            time.sleep(2.1)
            self.stop()
            time.sleep(1)
            self.direction(1)
            time.sleep(1)
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(1)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(1)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.2)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.2)        
            self.speed(40)
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)        
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)
            self.entkuppler3.actuate(0, 1, 0)
            time.sleep(0.1)
            time.sleep(3)  
            self.stop()      
            os._exit(0)
        
        elif (self.count32==2):
            self.stop()
            time.sleep(1000)
            os._exit(0)
        
    def entkuppeln3(self):
        self.count32=0
  
        self.direction(1)
        self.speed(30)
        

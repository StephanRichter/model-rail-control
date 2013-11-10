# coding=utf8
from lok import *
import time,os,srcp
import weichen
from weichen import ausfahrt3

class BR110(Lok):
    
    kpl=False
    
    def ankuppeln(self):
        self.direction(1)
        time.sleep(2)
        self.speed(60)
        time.sleep(15)
        self.stop()
        os._exit(0)
    
    def entkuppeln(self):
        # überfahren lassen
        time.sleep(2)
        self.stop()
        # anrücken
        time.sleep(1)
        self.direction(0)
        self.speed(1)
        time.sleep(0.4)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.entkuppler3.actuate(0, 1, 0)
        time.sleep(0.2)        
        self.direction(1)
        self.entkuppler3.actuate(0, 1,0)
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
        time.sleep(2)      
        self.weiche34.actuate(1, 1)
        time.sleep(1)
        self.einfahrt4()
        time.sleep(2)
        self.direction(0)
        self.speed(50)
            
    def pendelnVonGleis3(self):
        ausfahrt3()
        self.direction(0)
        self.speed(60)
        time.sleep(20)
        self.speed(128)
        time.sleep(30)
        self.stop()
    
    
    def action32(self):
        if (self.kpl):
            self.entkuppeln()
    
    def action64(self):
        if (self.kpl):
            self.stop()
            time.sleep(2)
            self.weiche34.actuate(0, 1)
            time.sleep(1)
            self.einfahrt3()
            time.sleep(2)
            self.ankuppeln()
                
    def entkuppeln3(self):
        self.kpl=True  
        self.direction(1)
        self.speed(30)
        

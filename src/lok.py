from thread import allocate_lock
import time
import srcp
class Lok:
    def __init__(self,lok):
        self.lok=lok
        lok.init('N', '1', 128, 4)
        
    lock16 = allocate_lock()
    act16 = False

    lock32 = allocate_lock()
    act32 = False
    
    lock64 = allocate_lock()
    act64 = False
        
    def action(self,contact):
        if (contact == 16):
            self.contact16()
        elif (contact == 32):
            self.contact32()
        elif (contact == 64):
            self.contact64()
        else:
            print "contact",contact 
            
    def action16(self):
        print "action 32"
        time.sleep(5)

    def action32(self):
        print "action 32"
        time.sleep(5)

    def action64(self):
        print "action 64"
        time.sleep(5)
            
    def contact16(self):
        self.lock16.acquire()
        if (self.act16):
            self.lock16.release();
            return
        self.act16 = True
        self.lock16.release();
        self.action16()
        self.lock16.acquire()
        self.act16 = False
        self.lock16.release();

    def contact32(self):
        self.lock32.acquire()
        if (self.act32):
            self.lock32.release();
            return
        self.act32 = True
        self.lock32.release();
        self.action32()
        self.lock32.acquire()
        self.act32 = False
        self.lock32.release();
        
    
    def contact64(self):
        self.lock64.acquire()
        if (self.act64):
            self.lock64.release();
            return
        self.act64 = True
        self.lock64.release();
        self.action64()
        self.lock64.acquire()
        self.act64 = False
        self.lock64.release();
        
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
        
        
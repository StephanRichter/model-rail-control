from thread import allocate_lock
import time
class Lok:
    def __init__(self,lok):
        self.lok=lok
        
    lock32 = allocate_lock()
    act32 = False
    
    lock64 = allocate_lock()
    act64 = False
        
    def action(self,contact):
        if (contact == 32):
            self.contact32()
        elif (contact == 64):
            self.contact64()
            
    def action32(self):
        print "action 32"
        time.sleep(5)

    def action64(self):
        print "action 64"
        time.sleep(5)
            
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
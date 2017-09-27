class SignalRoGeGr(object):
    def __init__(self,addr,chip,module):
        self.key="GA {}".format(addr)
        self.module=module
        self.chip=chip
        self.test()
        
    def red(self):
        print 'red'
        self.chip.sendSPI(0x13,0b00000001)
        
    def yellow(self):
        print 'yellow'
        self.chip.sendSPI(0x13,0b00000110)        
        
    def green(self):
        print 'green'
        self.chip.sendSPI(0x13,0b00000100)
        
    def test(self):
        self.chip.sendSPI(0x13,0b00000111)

        
    def respond(self,data):
        if self.key+" 1 1" in data:            
            self.red()
        if self.key+" 2 1" in data:
            self.green();
        if self.key+" 3 1" in data:
            self.yellow()    
            
    def respondsTo(self,data):        
        if self.key in data:
            self.respond(data)
            return True
        return False
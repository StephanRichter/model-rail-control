#!/usr/bin/python
from classes.SpiConnection import *

cable_select = 23
clock = 21
miso = 15
mosi = 19

conn = SpiConnection(cable_select,clock,mosi,miso)

chips=(conn.sensor(0),conn.sensor(2),conn.sensor(3))
old=0
while True:
    val=0
    for chip in (chips):
        val<<=16
        val = val|chip.readSPI()
        
        
    diff=old^val

    for i in range(16*len(chips),0,-1):
        if 1<<i-1 & diff:
            if 1<<i-1 & val:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
            else:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";
            
            print msg
    old=val
    
    time.sleep(0.01)

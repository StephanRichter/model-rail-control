# coding=utf8
from thread import start_new_thread
from lok import *
from ice import ICE
from br86 import BR86
from br110 import BR110
from br118 import BR118
from br130 import BR130
from mcp23s17 import *
from kontakte import *
import time,os

try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

SRCP_BUS=1    

commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

pause=6

BR86 = BR86(srcp.GL(SRCP_BUS,3))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR130 = BR130(srcp.GL(SRCP_BUS,8))
ICE = ICE(srcp.GL(SRCP_BUS, 1))

loks = [ BR110, BR86, BR118, BR130, ICE ]

for lok in loks:
    lok.direction(LINKS)
    lok.lichtAn()
    time.sleep(1)
    
BR86.status=PARKED
BR110.status=PARKED
BR118.status=PARKED
ICE.status=PARKED

BR130.status=EINGEFAHREN
BR130.bahnhof=LINKS
BR130.vonGleis=1
BR130.zuglaenge=82

def states():
    print        
    BR86.state()
    BR110.state()
    BR118.state()
    BR130.state()
    ICE.state()
    print
    
while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for lok in loks:
            start_new_thread(lok.action, (val,))    
    
    # folgende Zeilen sind zur Ablaufsteuerung
    
    if (BR86.stat(PARKED) & BR110.stat(PARKED) & BR118.stat(PARKED) & BR130.stat(EINGEFAHREN,LINKS,1) & ICE.stat(PARKED)):
        print "start!"
        break
    
    else:
        states()
        print "(Status nicht definiert)"
        print
        
        ICE.stop()
        BR110.stop()
        commandbus.powerOff()
        os._exit(0)
        

    time.sleep(0.01)

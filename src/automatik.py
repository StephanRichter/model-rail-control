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

pause=0

BR86 = BR86(srcp.GL(SRCP_BUS,3))
BR86.zuglaenge=55
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR118.zuglaenge=100

BR130 = BR130(srcp.GL(SRCP_BUS,5))
BR130.zuglaenge=82

ICE = ICE(srcp.GL(SRCP_BUS, 1))

loks = [ BR110, BR86, BR118, BR130, ICE ]

for lok in loks:
    lok.nachLinks()
    lok.lichtAn()

    
BR86.status=PARKED
BR110.status=PARKED
BR118.status=PARKED
BR130.status=PARKED
ICE.status=PARKED

BR118.status=BEREIT
BR118.bahnhof=LINKS
BR118.vonGleis=2



def states():
    print        
    BR86.state()
    BR110.state()
    BR118.state()
    BR130.state()
    ICE.state()
    print
    
statecount = 0

def reset():
    global statecount
    statecount=0
    
while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for lok in loks:
            start_new_thread(lok.action, (val,))    
    
    # folgende Zeilen sind zur Ablaufsteuerung
    
    if (BR86.stat(ABGEKUPPELT,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=UMFAHREN
        start_new_thread(BR86.umfahren, (pause,))
    elif (BR86.stat(ABGEKUPPELT,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=UMFAHREN
        start_new_thread(BR86.umfahren, (pause,))

    elif (BR86.stat(ABKUPPELN,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(ABKUPPELN,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(ANKUPPELN,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(ANKUPPELN,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(AUSFAHRT,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(AUSFAHRT,LINKS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(AUSFAHRT,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(BEREIT,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=GLEISWECHSEL
        BR86.nachGleis=2
        start_new_thread(BR86.gleiswechsel, (pause,))                
    elif (BR86.stat(BEREIT,LINKS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=AUSFAHRT
        BR86.nachGleis=2
        start_new_thread(BR86.ausfahrt, (pause,))                
    
    elif (BR86.stat(BEREIT,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=GLEISWECHSEL
        BR86.nachGleis=3
        start_new_thread(BR86.gleiswechsel, (pause,))                
    elif (BR86.stat(BEREIT,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=GLEISWECHSEL
        BR86.nachGleis=1
        start_new_thread(BR86.gleiswechsel, (pause,))                
    elif (BR86.stat(BEREIT,RECHTS,3) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=GLEISWECHSEL
        BR86.nachGleis=4
        start_new_thread(BR86.gleiswechsel, (pause,))                
    elif (BR86.stat(BEREIT,RECHTS,4) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=AUSFAHRT
        BR86.nachGleis=1
        start_new_thread(BR86.ausfahrt, (pause,))                

    elif (BR86.stat(EINFAHRT,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(EINFAHRT,LINKS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(EINFAHRT,LINKS,3) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(EINFAHRT,LINKS,4) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(EINFAHRT,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(EINFAHRT,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(EINGEFAHREN,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=ABKUPPELN
        start_new_thread(BR86.abkuppeln, (pause,))

    elif (BR86.stat(EINGEFAHREN,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR86.status=ABKUPPELN
        start_new_thread(BR86.abkuppeln, (pause,))

    elif (BR86.stat(GLEISWECHSEL,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(GLEISWECHSEL,LINKS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(GLEISWECHSEL,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(GLEISWECHSEL,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(GLEISWECHSEL,RECHTS,3) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(GLEISWECHSEL,RECHTS,4) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(NACH_LINKS,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(NACH_LINKS,RECHTS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(NACH_LINKS,RECHTS,3) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(NACH_LINKS,RECHTS,4) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    
    elif (BR86.stat(NACH_RECHTS,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(NACH_RECHTS,LINKS,2) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    ############################# BR 118
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=UMFAHREN
        start_new_thread(BR118.umfahren, (pause,))
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=UMFAHREN
        start_new_thread(BR118.umfahren, (pause,))
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ABKUPPELN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ABKUPPELN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ANKUPPELN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(ANKUPPELN,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(AUSFAHRT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(AUSFAHRT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(BEREIT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=GLEISWECHSEL
        BR118.nachGleis=2
        start_new_thread(BR118.gleiswechsel, (pause,))                
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(BEREIT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=AUSFAHRT
        BR118.nachGleis=2
        start_new_thread(BR118.ausfahrt, (pause,))                

        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=AUSFAHRT
        BR118.nachGleis=1
        start_new_thread(BR118.ausfahrt, (pause,))                
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(BEREIT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=GLEISWECHSEL
        BR118.nachGleis=1
        start_new_thread(BR118.gleiswechsel, (pause,))                
    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINFAHRT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINFAHRT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINFAHRT,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINFAHRT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=ABKUPPELN
        start_new_thread(BR118.abkuppeln, (pause,))

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        BR118.status=ABKUPPELN
        start_new_thread(BR118.abkuppeln, (pause,))

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(GLEISWECHSEL,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(GLEISWECHSEL,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(GLEISWECHSEL,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(GLEISWECHSEL,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(NACH_LINKS,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(NACH_LINKS,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(NACH_RECHTS,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(NACH_RECHTS,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

############################# BR 130

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(PARKED)):
        BR130.status=UMFAHREN
        start_new_thread(BR130.umfahren, (pause,))
    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABGEKUPPELT,RECHTS,2) and ICE.stat(PARKED)):
        BR130.status=UMFAHREN
        start_new_thread(BR130.umfahren, (pause,))

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(PARKED)):
        BR130.status=UMFAHREN
        start_new_thread(BR130.umfahren, (pause,))
    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABKUPPELN,LINKS,1) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABKUPPELN,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ABKUPPELN,RECHTS,3) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ANKUPPELN,LINKS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ANKUPPELN,RECHTS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ANKUPPELN,RECHTS,3) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(ANKUPPELN,RECHTS,4) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,LINKS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,LINKS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,RECHTS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,RECHTS,3) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(AUSFAHRT,RECHTS,4) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,LINKS,1) and ICE.stat(PARKED)):
        BR130.status=GLEISWECHSEL
        BR130.nachGleis=2
        start_new_thread(BR130.gleiswechsel, (pause,))                
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,LINKS,2) and ICE.stat(PARKED)):
        BR130.status=AUSFAHRT
        BR130.nachGleis=3
        start_new_thread(BR130.ausfahrt, (pause,))                

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,RECHTS,1) and ICE.stat(PARKED)):
        BR130.status=GLEISWECHSEL
        BR130.nachGleis=4
        start_new_thread(BR130.gleiswechsel, (pause,))
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,RECHTS,2) and ICE.stat(PARKED)):
        BR130.status=AUSFAHRT
        BR130.nachGleis=1
        start_new_thread(BR130.ausfahrt, (pause,))                
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,RECHTS,3) and ICE.stat(PARKED)):
        BR130.status=GLEISWECHSEL
        BR130.nachGleis=1
        start_new_thread(BR130.gleiswechsel, (pause,))
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(BEREIT,RECHTS,4) and ICE.stat(PARKED)):
        BR130.status=GLEISWECHSEL
        BR130.nachGleis=2
        start_new_thread(BR130.gleiswechsel, (pause,))

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,RECHTS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,LINKS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,LINKS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,LINKS,3) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINFAHRT,LINKS,4) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(PARKED)):
        BR130.status=ABKUPPELN
        start_new_thread(BR130.abkuppeln, (pause,))
    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINGEFAHREN,RECHTS,2) and ICE.stat(PARKED)):
        BR130.status=ABKUPPELN
        start_new_thread(BR130.abkuppeln, (pause,))
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(PARKED)):
        BR130.status=ABKUPPELN
        start_new_thread(BR130.abkuppeln, (pause,))

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,LINKS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,LINKS,2) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,RECHTS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,RECHTS,3) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(GLEISWECHSEL,RECHTS,4) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_LINKS,RECHTS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_LINKS,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_LINKS,RECHTS,3) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_LINKS,RECHTS,4) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_RECHTS,LINKS,1) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(NACH_RECHTS,LINKS,2) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(UMFAHREN,LINKS,1) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(UMFAHREN,RECHTS,1) and ICE.stat(PARKED)):
        reset()    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(UMFAHREN,RECHTS,2) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(UMFAHREN,RECHTS,3) and ICE.stat(PARKED)):
        reset()    
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(UMFAHREN,RECHTS,4) and ICE.stat(PARKED)):
        reset()
    
###################################### BR118
        
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(UMFAHREN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(UMFAHREN,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    elif (BR86.stat(PARKED) and BR110.stat(PARKED) and BR118.stat(UMFAHREN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

###################################### BR 86
    elif (BR86.stat(UMFAHREN,LINKS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()

    elif (BR86.stat(UMFAHREN,RECHTS,1) and BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED)):
        reset()
    else:
        statecount+=1
        print "undefinierter Zustand (",statecount,")"
        if (statecount > 5):
            states()
            print "(Status nicht definiert)"
            print
            
            ICE.stop()
            BR110.stop()
            commandbus.powerOff()
            os._exit(0)        

    time.sleep(0.01)

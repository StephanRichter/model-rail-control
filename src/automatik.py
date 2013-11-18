# coding=utf8
from thread import start_new_thread
from lok import *
from ice import ICE
from br110 import BR110
from br118 import BR118
from br86 import BR86
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

ICE = ICE(srcp.GL(SRCP_BUS, 1))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR86 = BR86(srcp.GL(SRCP_BUS,3))
BR118 = BR118(srcp.GL(SRCP_BUS,4))

loks = [ ICE, BR110, BR86, BR118 ]

for lok in loks:
    lok.direction(LINKS)
    lok.lichtAn()
    time.sleep(1)

#BR110.status=BEREIT_LINKS1
BR110.status=BEREIT_LINKS2
#BR110.status=BEREIT_RECHTS3
#BR110.status=BEREIT_RECHTS4
#BR110.status=EINFAHRT_LINKS1
#BR110.status=EINFAHRT_LINKS2
#BR110.status=EINFAHRT_RECHTS3
#BR110.status=EINFAHRT_RECHTS4
#BR110.status=EINGEFAHREN_LINKS1
#BR110.status=EINGEFAHREN_RECHTS3

ICE.status=BEREIT_LINKS1
#ICE.status=BEREIT_LINKS2
#ICE.status=BEREIT_RECHTS1
#ICE.status=BEREIT_RECHTS3
#ICE.status=BEREIT_RECHTS4

#BR86.status=BEREIT_LINKS1
#BR86.status=BEREIT_RECHTS1
#BR86.status=BEREIT_RECHTS2
BR86.status=BEREIT_RECHTS1
#BR86.status=EINGEFAHREN_LINKS1

#BR118.status=BEREIT_LINKS1
#BR118.status=BEREIT_RECHTS2
#BR118.status=EINGEFAHREN_LINKS1
BR118.status=BEREIT_RECHTS2

def states():
    print        
    BR110.state()
    ICE.state()
    BR86.state()
    BR118.state()
    print

    
while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for lok in loks:
            start_new_thread(lok.action, (val,))    
    
    # folgende Zeilen sind zur Ablaufsteuerung
    if   (( BR110.status == ANKUPPELN )
         &( ICE.status   == BEREIT_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == ANKUPPELN )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
        
    elif (( BR110.status == BEREIT_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):  
             
            states() 
            BR110.status=NACH_RECHTS3
            ICE.status=NACH_LINKS1
            states()
            start_new_thread(BR110.von1nachRechts3,(pause+5,))
            start_new_thread(ICE.von3nachLinks1,(pause+22,))

    elif (( BR110.status == BEREIT_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            states() 
            BR110.status=NACH_RECHTS3
            ICE.status=NACH_LINKS1
            states()
            start_new_thread(BR110.von1nachRechts3,(pause+5,))
            start_new_thread(ICE.von4nachLinks1,(pause+22,))
            
    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)): # hier
        BR110.status=NACH_RECHTS3    
        start_new_thread(BR110.von2nachRechts3, (pause,))

    
    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == BEREIT_RECHTS2)):
        BR86.status=WECHSEL_3_NACH_1
        start_new_thread(BR86.startWechsel3, (pause,))

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        BR118.status=KOPFMACHEN_RECHTS2
        start_new_thread(BR118.startEntkuppelnRechts, (pause,))
        
    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == KOPFMACHEN_RECHTS2)):
        pass        
    
    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == WECHSEL_NACH_1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == WECHSEL_3_NACH_1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        BR86.status=NACH_RECHTS2
        BR118.status=NACH_LINKS1
        start_new_thread(BR86.von1nachRechts2,(pause,))
        start_new_thread(BR118.von2nachLinks1,(pause+8,))

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        states() 
        BR86.status=NACH_LINKS1
        BR118.status=NACH_RECHTS2
        states()
        start_new_thread(BR86.von2nachLinks1, (pause,))   
        start_new_thread(BR118.von1nachRechts2, (pause,))  
        
    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINFAHRT_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINFAHRT_LINKS1)
         &( BR118.status == NACH_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINFAHRT_RECHTS2)
         &( BR118.status == EINFAHRT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINFAHRT_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        ICE.status=NACH_LINKS2
        BR110.status=NACH_RECHTS3
        start_new_thread(BR110.von2nachRechts3, (pause,))
        start_new_thread(ICE.von1nachLinks2, (pause+23,))

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)): 
        BR110.status=NACH_RECHTS4
        start_new_thread(BR110.von1nachRechts4, (pause,))

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == NACH_LINKS1)
         &( BR118.status == NACH_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == EINFAHRT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == NACH_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        ICE.status=NACH_RECHTS4
        states()
        start_new_thread(ICE.von1nachRechts,(pause+1,))        

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        BR86.status=NACH_RECHTS2
        BR118.status=NACH_LINKS1
        start_new_thread(BR86.von1nachRechts2,(pause,))
        start_new_thread(BR118.von2nachLinks1,(pause+8,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        states()
        ICE.status=NACH_RECHTS1
        start_new_thread(ICE.von2nachRechts,(pause,))

    elif (( BR110.status == BEREIT_RECHTS3)
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINFAHRT_RECHTS2)
         &( BR118.status == EINFAHRT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        ICE.status=NACH_RECHTS1
        start_new_thread(ICE.von2nachRechts, (pause,)) 

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        BR118.status=KOPFMACHEN_RECHTS2
        start_new_thread(BR118.startEntkuppelnRechts, (pause,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == KOPFMACHEN_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        BR86.status=KOPFMACHEN_RECHTS2
        start_new_thread(BR86.startEntkuppelnRechts2,(pause+1,))
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == KOPFMACHEN_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == EINFAHRT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == NACH_RECHTS2)
         &( BR118.status == NACH_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == ANKUPPELN)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == ANKUPPELN)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        BR110.status=NACH_LINKS2
        start_new_thread(BR110.von3nachLinks2,(pause,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        BR110.status=NACH_LINKS2
        start_new_thread(BR110.von3nachLinks2,(pause,))


    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        BR118.status=KOPFMACHEN_LINKS
        start_new_thread(BR118.startEntkuppelnLinks,(pause,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == KOPFMACHEN_LINKS)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        BR86.status=KOPFMACHEN_LINKS
        start_new_thread(BR86.startEntkuppelnLinks,(pause, ))
        
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == KOPFMACHEN_LINKS)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == ANKUPPELN)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        ICE.status=NACH_LINKS2
        states()
        start_new_thread(ICE.von4nachLinks2, (pause+1,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        BR86.status=NACH_LINKS1
        states()
        start_new_thread(BR86.von1nachLinks1,(pause+1,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == EINFAHRT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        BR86.status = KOPFMACHEN_LINKS
        start_new_thread(BR86.startEntkuppelnLinks,(pause, ))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == KOPFMACHEN_LINKS)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == NACH_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == EINFAHRT_LINKS2)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == EINFAHRT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == EINFAHRT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == EINFAHRT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == NACH_LINKS2)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == NACH_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == NACH_RECHTS1)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == NACH_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        ICE.status=NACH_RECHTS1
        start_new_thread(ICE.von2nachRechts,(pause,))
    
    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        BR86.status=KOPFMACHEN_RECHTS2
        start_new_thread(BR86.startEntkuppelnRechts2,(pause+1,))

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == KOPFMACHEN_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        BR86.status=WECHSEL_2_NACH_3
        start_new_thread(BR86.startWechsel2, (pause,))

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == BEREIT_LINKS1)): 
        BR118.status=NACH_RECHTS2
        start_new_thread(BR118.von1nachRechts2, (pause,))  

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        ICE.status=NACH_LINKS1
        BR110.status=NACH_LINKS2
        states()
        start_new_thread(BR110.von4nachLinks, (pause,True))
        start_new_thread(ICE.von1nachLinks, (pause,))


    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == NACH_RECHTS2)):
        pass        

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == ANKUPPELN)):
        pass        

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        ICE.status=NACH_LINKS2
        start_new_thread(ICE.von1nachLinks2, (pause,))

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):        
        BR118.status=KOPFMACHEN_LINKS
        start_new_thread(BR118.startEntkuppelnLinks,(pause,))

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == KOPFMACHEN_LINKS)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == WECHSEL_2_NACH_3)
         &( BR118.status == BEREIT_LINKS1)): 
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == WECHSEL_NACH_3)
         &( BR118.status == BEREIT_LINKS1)): 
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == EINFAHRT_LINKS2)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == EINFAHRT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == NACH_LINKS2)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == BEREIT_RECHTS4 )
         &( ICE.status   == NACH_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == EINFAHRT_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == EINFAHRT_LINKS1 )
         &( ICE.status   == EINFAHRT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == EINFAHRT_LINKS1 )
         &( ICE.status   == NACH_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == EINFAHRT_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        pass

    elif (( BR110.status == EINFAHRT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == EINFAHRT_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
            pass
        
    elif (( BR110.status == EINFAHRT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass

    elif (( BR110.status == EINFAHRT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
            pass

    elif (( BR110.status == EINFAHRT_RECHTS3 )
         &( ICE.status   == EINFAHRT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
            pass

    elif (( BR110.status == EINFAHRT_RECHTS3 )
         &( ICE.status   == NACH_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
            pass

    elif (( BR110.status == EINGEFAHREN_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        BR110.status=KOPFMACHEN_LINKS
        states()
        start_new_thread(BR110.startEntkuppelnLinks,(pause+5,))
    
    elif (( BR110.status == EINGEFAHREN_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        BR110.status=KOPFMACHEN_LINKS
        states()
        start_new_thread(BR110.startEntkuppelnLinks,(pause+5,))
    
    elif (( BR110.status == EINGEFAHREN_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        states()
        BR110.status=KOPFMACHEN_RECHTS3
        states()
        start_new_thread(BR110.startEntkuppelnRechts,(pause+5,))
    
    elif (( BR110.status == KOPFMACHEN_LINKS )
         &( ICE.status   == BEREIT_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass    
    
    elif (( BR110.status == KOPFMACHEN_LINKS )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == KOPFMACHEN_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == NACH_LINKS1 )
         &( ICE.status   == EINFAHRT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == NACH_LINKS1 )
         &( ICE.status   == NACH_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass
    
    elif (( BR110.status == NACH_LINKS1 )
         &( ICE.status   == NACH_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass
        
    elif (( BR110.status == NACH_LINKS2 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        pass

    elif (( BR110.status == NACH_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == NACH_LINKS2 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == BEREIT_RECHTS2)
         &( BR118.status == BEREIT_LINKS1)):
        pass

    elif (( BR110.status == NACH_LINKS2 )
         &( ICE.status   == EINFAHRT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        pass

    elif (( BR110.status == NACH_LINKS2 )
         &( ICE.status   == NACH_LINKS1)
         &( BR86.status  == BEREIT_RECHTS3)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
        pass

    elif (( BR110.status == NACH_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == NACH_RECHTS3 )
         &( ICE.status   == EINFAHRT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == NACH_RECHTS3 )
         &( ICE.status   == EINFAHRT_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
            pass
        
    elif (( BR110.status == NACH_RECHTS3 )
         &( ICE.status   == NACH_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass

    elif (( BR110.status == NACH_RECHTS3 )
         &( ICE.status   == NACH_LINKS2)
         &( BR86.status  == EINGEFAHREN_LINKS1)
         &( BR118.status == EINGEFAHREN_RECHTS2)):
            pass
        
    elif (( BR110.status == NACH_RECHTS4 )
         &( ICE.status   == BEREIT_RECHTS1)
         &( BR86.status  == EINGEFAHREN_RECHTS2)
         &( BR118.status == EINGEFAHREN_LINKS1)):
        pass
    
    else:
        states()
        print "(Status nicht definiert)"
        print
        
        ICE.stop()
        BR110.stop()
        commandbus.powerOff()
        os._exit(0)
        

    time.sleep(0.01)

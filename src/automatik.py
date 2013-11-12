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

pause=0

ICE = ICE(srcp.GL(SRCP_BUS, 1))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR86 = BR86(srcp.GL(SRCP_BUS,3))
BR118 = BR118(srcp.GL(SRCP_BUS,4))

loks = [ ICE, BR110, BR86, BR118 ]

BR86.status=BEREIT_LINKS1
#BR86.status=BEREIT_RECHTS1
#BR86.status=EINGEFAHREN_LINKS1

#BR110.status=BEREIT_LINKS1
BR110.status=BEREIT_RECHTS3
#BR110.status=EINFAHRT_LINKS1
#BR110.status=EINGEFAHREN_LINKS1
#BR110.status=EINGEFAHREN_RECHTS3

BR118.status=BEREIT_RECHTS2

ICE.status=BEREIT_LINKS2
#ICE.status=BEREIT_RECHTS3
#ICE.status=BEREIT_RECHTS4

    
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
              
            BR110.status=NACH_RECHTS3
            ICE.status=NACH_LINKS1
            start_new_thread(BR110.von1nachRechts3,(pause+5,))
            start_new_thread(ICE.von3nachLinks1,(pause+22,))

    elif (( BR110.status == BEREIT_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            BR110.status=NACH_RECHTS3
            ICE.status=NACH_LINKS1
            start_new_thread(BR110.von1nachRechts3,(pause+5,))
            start_new_thread(ICE.von4nachLinks1,(pause+22,))
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            ICE.status=NACH_RECHTS4
            start_new_thread(ICE.von1nachRechts4,(pause+1,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS2)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
        BR86.status=NACH_RECHTS2
        BR118.status=NACH_LINKS1
        start_new_thread(BR86.von1nachRechts2,(pause,)) # hier gehts weiter
        start_new_thread(BR118.von2nachLinks1,(pause+8,))

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
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == ANKUPPELN)
         &( BR118.status == BEREIT_RECHTS2)):
        pass
    
    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_LINKS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
        ICE.status=NACH_LINKS2
        start_new_thread(ICE.von4nachLinks2, (pause+1,))

    elif (( BR110.status == BEREIT_RECHTS3 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
        BR86.status=NACH_LINKS1
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
         &( ICE.status   == NACH_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
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

    elif (( BR110.status == EINGEFAHREN_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS3)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            BR110.status=KOPFMACHEN_LINKS
            start_new_thread(BR110.startEntkuppelnLinks,(pause+5,))
    
    elif (( BR110.status == EINGEFAHREN_LINKS1 )
         &( ICE.status   == BEREIT_RECHTS4)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            BR110.status=KOPFMACHEN_LINKS
            start_new_thread(BR110.startEntkuppelnLinks,(pause+5,))
    
    elif (( BR110.status == EINGEFAHREN_RECHTS3 )
         &( ICE.status   == BEREIT_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
        
            BR110.status=KOPFMACHEN_RECHTS3
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
         &( ICE.status   == NACH_LINKS1)
         &( BR86.status  == BEREIT_RECHTS1)
         &( BR118.status == BEREIT_RECHTS2)):
            pass
    
    else:
        print        
        BR110.state()
        ICE.state()
        BR86.state()
        BR118.state()
        print
        print "(Status nicht definiert)"
        print
        
        ICE.stop()
        BR110.stop()
        commandbus.powerOff()
        os._exit(0)
        

    time.sleep(0.01)

from thread import start_new_thread
from lok import *
from ice import ICE
from br110 import BR110
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

ICE = ICE(srcp.GL(SRCP_BUS, 1))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
loks = [ ICE, BR110 ]

ICE.status=BEREIT_LINKS1
ICE.status=BEREIT_RECHTS4
BR110.status=EINGEFAHREN_RECHTS3
BR110.status=EINGEFAHREN_LINKS1

#ICE.status=2
#BR110.status=3
    
while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for lok in loks:
            start_new_thread(lok.action, (val,))
        
    # folgende Zeilen sind zur Ablaufsteuerung
    if   ((BR110.status== ANKUPPELN )&(ICE.status==BEREIT_RECHTS4)):
        pass
    
    elif ((BR110.status== BEREIT_LINKS1 ) & (ICE.status==BEREIT_RECHTS3)):
        
        BR110.status=NACH_RECHTS3
        ICE.status=NACH_LINKS1
        start_new_thread(BR110.von1nachRechts3,(5,))
        start_new_thread(ICE.von3nachLinks1,(15,))

    elif ((BR110.status== BEREIT_LINKS1 ) & (ICE.status==BEREIT_RECHTS4)):
        
        BR110.status=NACH_RECHTS3
        ICE.status=NACH_LINKS1
        start_new_thread(BR110.von1nachRechts3,(5,))
        start_new_thread(ICE.von4nachLinks1,(15,))
    
    elif ((BR110.status== BEREIT_RECHTS3 ) & (ICE.status==BEREIT_LINKS1)):
        
        BR110.status=NACH_LINKS1
        ICE.status=NACH_RECHTS4
        start_new_thread(BR110.von3nachLinks1,(1,))
        start_new_thread(ICE.von1nachRechts4,(20,))
    
    elif ((BR110.status==EINFAHRT_LINKS1 )&(ICE.status==NACH_RECHTS4)):
        pass

    elif ((BR110.status== EINGEFAHREN_LINKS1 ) & (ICE.status==BEREIT_RECHTS4)):
        
        BR110.status=KOPFMACHEN_LINKS
        start_new_thread(BR110.startEntkuppelnLinks,(5,))
    
    elif ((BR110.status== EINGEFAHREN_RECHTS3 ) & (ICE.status==BEREIT_LINKS1)):
        
        BR110.status=KOPFMACHEN_RECHTS3
        start_new_thread(BR110.startEntkuppelnRechts,(5,))
    
    elif ((BR110.status== KOPFMACHEN_LINKS )&(ICE.status==BEREIT_RECHTS4)):
        pass
    
    elif ((BR110.status== KOPFMACHEN_RECHTS3 )&(ICE.status==BEREIT_LINKS1)):
        pass

    elif ((BR110.status== NACH_LINKS1 )&(ICE.status==NACH_RECHTS3)):
        pass
    
    elif ((BR110.status== NACH_LINKS1 )&(ICE.status==NACH_RECHTS4)):
        pass
    
    elif ((BR110.status== NACH_RECHTS3 )&(ICE.status==BEREIT_LINKS1)):
        pass

    elif ((BR110.status== NACH_RECHTS3 )&(ICE.status==EINFAHRT_LINKS1)):
        pass

    elif ((BR110.status== NACH_RECHTS3 )&(ICE.status==NACH_LINKS1)):
        pass
    
    else:
        print "Status nicht definiert:"
        print "BR110 =", BR110.status
        print "ICE =", ICE.status
        
        ICE.stop()
        BR110.stop()
        commandbus.powerOff()
        time.sleep(2)        
        os._exit(0)
        

    time.sleep(0.01)

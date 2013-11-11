from thread import start_new_thread, allocate_lock
from ice import *
from br110 import *
from mcp23s17 import *
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

gleis34=srcp.GA(SRCP_BUS,8)

ICE.status=Lok.BEREIT_RECHTS3
BR110.status=Lok.EINGEFAHREN_LINKS1
#BR110.direction(1)
#BR110.speed(128)
#time.sleep(3)
#BR110.stop()

#start_new_thread(BR110.pendelnVonGleis3,())

# Programmierung der Pins
    
while True:
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for lok in loks:
            start_new_thread(lok.action, (val,))
        
    # folgende Zeilen sind zur Ablaufsteuerung
    if ((BR110.status==Lok.BEREIT_LINKS1) & (ICE.status==Lok.BEREIT_RECHTS3)):
        BR110.status=Lok.NACH_RECHTS3
        ICE.status=Lok.NACH_LINKS1
        start_new_thread(BR110.von1nachRechts3,(25,))
        start_new_thread(ICE.von3nachLinks1,(35,))
    elif ((BR110.status==Lok.EINGEFAHREN_RECHTS3) & (ICE.status==Lok.BEREIT_LINKS1)):
        BR110.status=Lok.KUPPLUNG_AKTIV
        start_new_thread(BR110.startEntkuppelnRechts,(25,))
    elif ((BR110.status==Lok.BEREIT_RECHTS3) & (ICE.status==Lok.BEREIT_LINKS1)):
        BR110.status=Lok.NACH_LINKS1
        ICE.status=Lok.NACH_RECHTS3
        start_new_thread(BR110.von3nachLinks1,(21,))
        start_new_thread(ICE.von1nachRechts3,(40,))
    elif ((BR110.status==Lok.EINGEFAHREN_LINKS1) & (ICE.status==Lok.BEREIT_RECHTS3)):
        BR110.status=Lok.KOPFMACHEN_LINKS
        start_new_thread(BR110.startEntkuppelnLinks,(25,))
        

    time.sleep(0.01)

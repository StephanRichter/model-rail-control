# coding=utf8
from thread import start_new_thread
from train import *
from br86 import BR86
from br110 import BR110
from br118 import BR118
from br130 import BR130
from ice import ICE
from mcp23s17 import *
from constants import *
import time,os,random
import br110
from numpy.matlib import rand
from station import Station
from platf import Platform

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
BR110.zuglaenge=82
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR118.zuglaenge=100

BR130 = BR130(srcp.GL(SRCP_BUS,5))
BR130.zuglaenge=82

ICE = ICE(srcp.GL(SRCP_BUS, 1))

trains = [ BR110, BR86, BR118, BR130, ICE ]

for train in trains:
    train.nachLinks()
    train.lichtAn()
    time.sleep(0.01)
    
l2=Platform("Gleis 2",124)
l1=Platform("Gleis 1",124)
l1.setBypass(l1)

r1=Platform("Gleis 1",130)
r2=Platform("Gleis 2",130)
r3=Platform("Gleis 3",120)
r4=Platform("Gleis 4",120)
r2.setBypass(r1,97)
r3.setBypass(r4,87)

bahnhofLinks=Station("Bahnhof Links")
bahnhofLinks.addPlatform(l1)
bahnhofLinks.addPlatform(l2)
bahnhofLinks.addContact(KONTAKT_EINFAHRT_LINKS)
bahnhofLinks.addContact(KONTAKT_ENTKUPPLER_LINKS)

bahnhofRechts=Station("Bahnhof Rechts")
bahnhofRechts.addPlatform(r1)
bahnhofRechts.addPlatform(r2)
bahnhofRechts.addPlatform(r3)
bahnhofRechts.addPlatform(r4)
bahnhofRechts.addContact(KONTAKT_EINFAHRT_RECHTS)
bahnhofRechts.addContact(KONTAKT_ENTKUPPLER_RECHTS2)
bahnhofRechts.addContact(KONTAKT_ENTKUPPLER_RECHTS3)

BR86.setState(l1,EINGEFAHREN)
BR110.setState(l2,BEREIT)
BR118.setState(r4,BEREIT)
BR130.setState(r3,ABGEKUPPELT)
ICE.setState(r1,BEREIT)

stations=[bahnhofLinks,bahnhofRechts]

while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for station in stations:
            start_new_thread(station.contact, (val,))
            time.sleep(1)    
    
    # folgende Zeilen sind zur Ablaufsteuerung
    
#    if activeTrains==0:
#        train1=random.choice(trains)
#        train2=random.choice(trains)
#        if train1==train2:
#            print "only train 1",
#            print train1
#        else:
#            print train1
#            print train2

    time.sleep(0.01)

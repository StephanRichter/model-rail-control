# coding=utf8
from thread import start_new_thread
from mcp23s17 import *
import time
from myconsts import *
from environ import *
from platf import *
from station import *
from train import *
from br86 import BR86
from br110 import BR110
from br118 import BR118
from br130 import BR130
from ice import ICE
import random

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
BR86.trainlength=55
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR110.trainlength=82
BR110.pushpull=True
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR118.trainlength=100

BR130 = BR130(srcp.GL(SRCP_BUS,5))
BR130.trainlength=82

ICE = ICE(srcp.GL(SRCP_BUS, 1))
ICE.trainlength=122
ICE.pushpull=True
trains = [ BR110, BR86, BR118, BR130, ICE ]

for train in trains:
    train.nachLinks()
    train.lichtAn()
    time.sleep(0.01)
    
BR86.setState(l1,EINGEFAHREN)
BR110.setState(l2,BEREIT)
BR118.setState(r4,BEREIT)
BR130.setState(r3,ABGEKUPPELT)
ICE.setState(r1,BEREIT)

stations=[bahnhofLinks,bahnhofRechts]

activeTrains=[]

def tryAction(train):
    global activeTrains
    if train.status==EINGEFAHREN:
        train.startAbkuppeln(pause)
        time.sleep(1)
        while train.status!=ABGEKUPPELT:
            time.sleep(1)
    elif train.status==BEREIT:
        targetPlatforms=train.possibleTargets()
        print train
        availableTargets=[]
        for target in targetPlatforms:            
            if target.isFree():
                availableTargets.append(target)
        if availableTargets:
            target=random.choice(availableTargets)
            train.startAusfahrt(target,pause)
        else:
            print "no target available"
    else:
        activeTrains=[]        

def tryCrossing(train1,train2):
    global activeTrains
    if train1.station==train2.station:
        activeTrains=[]
        return 
    if train1.status!=BEREIT:
        activeTrains=[]
        return
    if train2.status!=BEREIT:
        activeTrains=[]
        return
    activeTrains=[]
    print "Wechsel von",train1,"und",train2,"sollte gehen"

while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for train in trains:
            start_new_thread(train.contact,(val,))
    
    # folgende Zeilen sind zur Ablaufsteuerung
    
    if not activeTrains:
        train1=random.choice(trains)
        train2=random.choice(trains)
        if train1==train2:
            activeTrains.append(train1)
            start_new_thread(tryAction,(train1,))
        else:
            activeTrains.append(train1)
            activeTrains.append(train2)
            start_new_thread(tryCrossing,(train1,train2))

    time.sleep(0.01)

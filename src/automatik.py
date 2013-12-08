#!/usr/bin/python
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
import sys
import select
import tty
import termios
from pydoc import deque

try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

SRCP_BUS=1    

commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

pause=10

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
ICE.trainlength=119
ICE.pushpull=True
trains = [ BR110, BR86, BR118, BR130, ICE ]


BR110.setState(r4 , BEREIT)

for train in trains:
    if train.status==UNDEFINED:
        train.loadState()
    train.state()

activeTrains=[]

def keyPressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def tryAction(train):
    global activeTrains
    if train.status==ABGEKUPPELT:        
        if train.platform.bypass==None:
            print "Achtung:",train,"ist abgekuppelt, hat aber kein Gleis zum umfahren!?"
            return
        elif train.platform.bypass.isFree():
            train.startUmfahren(pause)
            time.sleep(2)
            while train.status!=BEREIT:
                time.sleep(1)
        else:
            print "Umfahrungsgleis für",train,"nicht frei."                
    elif train.status==BEREIT:
        targetPlatforms=train.possibleTargets()
        availableTargets=[]
        for target in targetPlatforms:
            if target.isFree():
                availableTargets.append(target)
        if availableTargets:
            target=random.choice(availableTargets)
            train.startAusfahrt(target,pause)
            time.sleep(1)
            while train.status!=BEREIT and train.status!=EINGEFAHREN:
                time.sleep(1)        
        else:
            
            if train.lastaction!=GLEISWECHSEL:
                availableTargets=train.station.freePlatforms()
                if availableTargets:
                    target=random.choice(availableTargets)
                    train.startGleiswechsel(target,pause)
                    time.sleep(1)
                    while train.status!=BEREIT and train.status!=EINGEFAHREN:
                        time.sleep(1)        
                else:
                    print "kein Zielgleis frei für",train
            else:
                print train,"hat schon einmal das Gleis gewechselt"
    elif train.status==EINGEFAHREN:
        train.startAbkuppeln(pause)
        time.sleep(1)
        while train.status!=ABGEKUPPELT:
            time.sleep(1)
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
    
    targets=train1.possibleTargets()
    available1=[]
    for platform in targets:
        train=platform.train
        if train==train2 or train==None:
            available1.append(platform)
            
    targets=train2.possibleTargets()
    available2=[]
    for platform in targets:
        train=platform.train
        if train==train1 or train==None:
            available2.append(platform)
    print "Wechsel von",train1,"und",train2,"?"
    if available1:
        if available2:
            target1=random.choice(available1)
            target2=random.choice(available2)
            pause1=pause
            if train1==BR86:
                pause1=pause+2
            elif train1==BR118:
                pause1=pause+6
            elif train1==BR130:
                pause1=pause+3
            elif train1==ICE:
                pause1=pause+13
            pause2=pause
            if train2==BR86:
                pause2=pause+2
            elif train2==BR118:
                pause2=pause+6
            elif train2==BR130:
                pause2=pause+3
            elif train2==ICE:
                pause2=pause+13
            train1.startAusfahrt(target1,pause1)
            train2.startAusfahrt(target2,pause2)
            time.sleep(1)
            while (train1.status!=BEREIT and train1.status!=EINGEFAHREN) or (train2.status!=BEREIT and train2.status!=EINGEFAHREN):
                time.sleep(1)
        else:
            print "Kein Zielgleis für",train2
    else:
        print "Kein Zielgleis für",train1    
    activeTrains=[]

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

trainqueue = deque([])

def nextTrain():
    if len(trainqueue)==0:
        return random.choice(trains)
    return trainqueue.popleft()

def queTrain(train):
    print "putting ",train,"in the queue." 
    trainqueue.append(train)
    

while True:    
    sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val != 0):
        for train in trains:
            start_new_thread(train.contact,(val,))
    
    # folgende Zeilen sind zur Ablaufsteuerung
    if keyPressed():
        c = sys.stdin.read(1)
        if c == 'q':
            break
        elif c == ' ':
            break
        elif c == '1':
            queTrain(ICE)
        elif c == '2':
            queTrain(BR110)
        elif c == '3':
            queTrain(BR130)
        elif c == '8':
            queTrain(BR118)
        elif c == '6':
            queTrain(BR86)
            
    if not activeTrains:
        train1=nextTrain()
        train2=nextTrain()                
        if train1!=train2 and random.choice([1,2])==1:        
            activeTrains.append(train1)
            activeTrains.append(train2)
            start_new_thread(tryCrossing,(train1,train2))
        else:
            activeTrains.append(train1)            
            start_new_thread(tryAction,(train1,))

    time.sleep(0.01)

commandbus.powerOff()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
for train in trains:
    train.writeState()
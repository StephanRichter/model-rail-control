#!/usr/bin/python
# coding=utf8

from train import *
from track import *
from mcp23s17 import *
import select,sys,termios,tty,random

try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()
    
stopListeners=dict()
print

def triggerContacts(input):
    print input
    if input&16:
        trn=stopListeners[16]
        if trn:
            trn.stop()        
    if input&32:
        trn=stopListeners[32]
        if trn:
            trn.stop()        
    if input&64:
        trn=stopListeners[64]
        if trn:
            trn.stop()
    if input&128:
        trn=stopListeners[128]
        if trn:
            trn.stop()
    
def keyPressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def stopOn(train,track):
    print train,"=>",track
    stopListeners[track.getContact()]=train
    
def stelle(weichenstr):
    for w in weichenstr:
        if (w<0):            
            weichen[-w].actuate(0,1,500)
        else:
            weichen[w].actuate(1,1,500)
        

SRCP_BUS=1
commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

# Weichen

weichen=dict()
for i in range(8):
    weiche=srcp.GA(SRCP_BUS,i+1)
    weiche.init("N")
    weichen[i+1]=weiche

# Wagen

doppelstockeinheit_lang=Waggon(60)
doppelstockeinheit_kurz=Waggon(30)
gueterwaggons=Waggon(100)
personenwagen=Waggon(120)

# Züge

doppelstockzug_lang=[doppelstockeinheit_lang]
doppelstockzug_kurz=[doppelstockeinheit_kurz]
gueterzug=[gueterwaggons]
personenzug=[personenwagen]

# Loks

loks=[]
ICE=Loco(SRCP_BUS,1,"ICE",10,10) # Längen korrigieren
loks.append(ICE)
BR110=Loco(SRCP_BUS,2,"BR110",5,5)
loks.append(BR110)
BR86=Loco(SRCP_BUS,3,"BR 86",5,5)
loks.append(BR86)
BR118=Loco(SRCP_BUS,4,"BR 118",5,5)
loks.append(BR118)
BR130=Loco(SRCP_BUS,5,"BR130",5,5)
loks.append(BR130)

# Züge
BR110.appendB(doppelstockzug_lang)  
BR86.appendA(doppelstockzug_kurz)
BR118.appendA(personenzug)
BR130.appendA(gueterzug)

# Gleise
track1=Track("Abstellbahnhof vorn/1")
track1.setTurnouts([-1])
track2=Track("Abstellbahnhof vorn/2")
track2.setTurnouts([1,-2])
track3=Track("Abstellbahnhof vorn/3")
track3.setTurnouts([1,2,-3])
track3.setContact(64)
track4=Track("Abstellbahnhof vorn/4")
track4.setTurnouts([1,2,3,-4])
track4.setContact(128)
track5=Track("Abstellbahnhof vorn/5")
track5.setContact(16)
track5.setTurnouts([1,2,3,4,-5])
track6=Track("Abstellbahnhof vorn/6")
track6.setContact(32)
track6.setTurnouts([1,2,3,4,5])

track3.connectTo(track4)
track3.connectTo(track6)

track4.connectTo(track3)
track4.connectTo(track6)

track6.connectTo(track3)
track6.connectTo(track4)

track1.setTrain(BR118)
track2.setTrain(BR130)
track4.setTrain(BR110)
track5.setTrain(ICE)
track6.setTrain(BR86)

tracks=[track1,track2,track3,track4,track5,track6]

###### MAIN ######

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

quit=False
active=False
while True:
    sendSPI(SPI_SLAVE_ADDR,SPI_GPIOB,ledPattern)
    val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
    if (val!=0):
        triggerContacts(val)
    
    if keyPressed():
        c = sys.stdin.read(1)
        if c == 'q':
            quit=True
            print "Programm wird im nächsten betriebssicheren Zustand angehalten." 
        elif c == ' ':
            break

    if not active:
        trck=random.choice(tracks)
        trn=trck.getTrain()
        if trn:        
            targs=trck.getFreeTargets()            
            if targs:
                target=random.choice(targs)
                if target:
                    stelle(target.getTurnouts())                    
                    stopOn(trn,target)
                    trn.setSpeed(128)                    
                    active=True
        
    if quit:
        break        
    time.sleep(0.01)

for lok in loks:
    lok.stop()
commandbus.powerOff()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

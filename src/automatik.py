# coding=utf8
from thread import start_new_thread
from lok import *
from br86 import BR86
from br110 import BR110
from br118 import BR118
from br130 import BR130
from ice import ICE
from mcp23s17 import *
from kontakte import *
import time,os,random
import br110

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

loks = [ BR110, BR86, BR118, BR130, ICE ]

for lok in loks:
    lok.nachLinks()
    lok.lichtAn()

    
BR86.status=BEREIT
BR86.bahnhof=RECHTS
BR86.vonGleis=3

BR110.status=BEREIT
BR110.bahnhof=RECHTS
BR110.vonGleis=4

BR118.status=ABGEKUPPELT
BR118.bahnhof=RECHTS
BR118.vonGleis=2

BR130.status=EINGEFAHREN
BR130.bahnhof=LINKS
BR130.vonGleis=1

ICE.status=BEREIT
ICE.bahnhof=RECHTS
ICE.vonGleis=1


def states():
    print        
    BR86.state()
    BR110.state()
    BR118.state()
    BR130.state()
    ICE.state()
    print

states()
    
statecount = 0

def err():
    global statecount
    statecount+=1

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
    
    if BR86.stat(ABGEKUPPELT,LINKS,1):
        if BR110.stat(AUSFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    rand=random.choice([1,2,3,4])
                    rand=3
                    print "z111"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(4,pause)
                    else:
                        BR130.startUmfahren(pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3])
                    rand=4
                    print "z125"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    else:
                        BR110.startAusfahrt(2,pause)
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    rand=random.choice([1,2,3,4])
                    rand=2
                    print "z100"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(4,pause)
                    else:
                        BR130.startAbkuppeln(pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3,4])
                    rand=2
                    print "z119"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                    else:
                        BR130.startAbkuppeln(pause)
                else:
                    err()
            else:
                err()
            
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5])
                    rand=4
                    print "z143"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause+13)
                    elif rand==4:
                        BR130.startUmfahren(pause)
                    else:
                        ICE.startAusfahrt(4,pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3])
                    rand=2
                    print "z207"
                    print "rand =",rand
                    if rand==1:
                        BR86.startUmfahren(pause)
                    elif rand==2:
                        BR110.startAusfahrt(2, pause)
                    else:
                        ICE.startAusfahrt(2,pause)                    
                else:
                    err()
            elif BR130.stat(ABKUPPELN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                rand=4
                print "z101"
                print "rand = ",rand
                if rand==1:
                    BR110.startGleiswechsel(4,pause)
                elif rand==2:
                    BR110.startAusfahrt(2, pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(2, pause)
                    ICE.startAusfahrt(4,pause+13)                
                elif rand==4:
                    BR130.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(4,pause)
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4])
                    rand=4
                    print "z182"
                    print "rand = ",rand
                    if rand==1:
                        BR110.startGleiswechsel(2,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(4,pause+13)                
                    else:
                        ICE.startAusfahrt(2,pause)                
                elif BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5])
                    rand=1
                    print "z118"
                    print "rand = ",rand
                    if rand==2:
                        BR110.startGleiswechsel(2,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(4,pause+13)                
                    elif rand==4:
                        BR130.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4])
                rand=2
                print "z277"
                print "rand =",rand
                if rand==1:
                    BR86.startUmfahren(pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(2,pause)
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,4) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(EINFAHRT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(BEREIT,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()                        
        elif BR110.stat(GLEISWECHSEL,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,4) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,4) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):                
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):                
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(NACH_RECHTS,LINKS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            start_new_thread(BR86.umfahren, (pause,))
        else:
            err()
    elif BR86.stat(ABGEKUPPELT,RECHTS,2):
        if BR110.stat(AUSFAHRT,LINKS,2) and BR118.stat(NACH_LINKS,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(BEREIT,LINKS,1) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            rand=random.choice([1,2,3,4,5])
            rand=2
            print "z441"
            print "rand =",rand
            if rand==1:
                BR110.startGleiswechsel(2,pause)
            elif rand==2:
                BR110.startAusfahrt(1,pause)
                BR118.startAusfahrt(1, pause+5)
            elif rand==3:
                BR110.startAusfahrt(4,pause)
                ICE.startAusfahrt(1,pause+13)
            elif rand==4:
                BR110.startAusfahrt(4,pause)
                ICE.startAusfahrt(2,pause+13)
            else:
                ICE.startAusfahrt(2,pause)
        elif BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                rand=random.choice([1,2,3,4,5,6])
                rand=3
                print "z459"
                print "rand =",rand
                if rand==1:
                    BR110.startGleiswechsel(1,pause)
                elif rand==2:
                    BR110.startAusfahrt(1, pause)
                    BR118.startAusfahrt(1,pause+5)
                elif rand==3:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+1)
                elif rand==5:
                    BR118.startAusfahrt(1,pause)
                else:
                    ICE.startAusfahrt(1,pause)
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                rand=random.choice([1,2,3,4,5])
                rand=1
                print "z482"
                print "rand=",rand
                if rand==1:
                    BR86.startUmfahren(pause)
                elif rand==2:
                    BR110.startAusfahrt(1,pause)
                elif rand==3:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startGleiswechsel(1, pause)
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            rand=random.choice([1,2,3])
            rand=1
            print "z481"
            print "rand =",rand
            if rand==1:
                BR110.startAusfahrt(2,pause)
            elif rand==2:
                BR118.startAbkuppeln(pause)
            else:
                ICE.startAusfahrt(2,pause)
        elif BR110.stat(EINFAHRT,LINKS,1) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(EINFAHRT,RECHTS,2):
            if BR118.stat(EINFAHRT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,LINKS,1) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(GLEISWECHSEL,LINKS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,1) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(NACH_RECHTS,LINKS,2):
            if BR118.stat(NACH_LINKS,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            elif BR118.stat(EINFAHRT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            else:
                err()                
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            start_new_thread(BR86.umfahren, (pause,))
        else:
            err()

    elif BR86.stat(ABGEKUPPELT,RECHTS,3):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            rand=random.choice([1,2,3,4,5])
            rand=2
            print "z555"
            print "rand =",rand
            if rand==1:
                BR86.startUmfahren(pause)
            elif rand==2:
                BR110.startAusfahrt(1,pause)
                ICE.startAusfahrt(2,pause+13)
            elif rand==3:
                BR110.startAusfahrt(4,pause)
                ICE.startAusfahrt(2,pause+13)
            elif rand==4:
                BR130.startAbkuppeln(pause)
            else:
                ICE.startGleiswechsel(4,pause)
                
        elif BR110.stat(BEREIT,RECHTS,2):
            if BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                if rand==1:
                    start_new_thread(BR86.umfahren, (pause,))
                elif rand==2:
                    BR110.startGleiswechsel(4,pause)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(4,pause+13)
                else:
                    ICE.startAusfahrt(4,pause)                    
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(BEREIT,LINKS,2):
                        rand=random.choice([1,2,3,4,5])
                        if rand==1:
                            BR110.startGleiswechsel(2,pause)
                        elif rand==2:
                            BR110.startAusfahrt(2,pause)
                            ICE.startAusfahrt(2,pause+13)
                        elif rand==3:
                            BR110.startAusfahrt(2,pause)
                            ICE.startAusfahrt(4,pause+13)
                        elif rand==4:
                            BR118.startGleiswechsel(2, pause)
                        else:
                            ICE.startAusfahrt(2,pause)
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,4) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        else:
            err()

    elif BR86.stat(ABKUPPELN,LINKS,1):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
            reset()
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    
    elif BR86.stat(ABKUPPELN,RECHTS,2):
        if BR110.stat(BEREIT,LINKS,1) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(ABKUPPELN,RECHTS,3):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(EINGEFAHREN,LINKS,1):
                    if (ICE.stat(BEREIT,LINKS,2)):
                        pass
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
        else:
            err()

    elif BR86.stat(ANKUPPELN,LINKS,1):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(ANKUPPELN,RECHTS,1):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(ANKUPPELN,RECHTS,4):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        else:
            err()

    elif BR86.stat(AUSFAHRT,LINKS,1):
        if BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(NACH_LINKS,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(AUSFAHRT,LINKS,2):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
        else:
            err()

    elif BR86.stat(AUSFAHRT,RECHTS,1):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
        else:
            err()

    elif BR86.stat(BEREIT,LINKS,1):
        if BR110.stat(AUSFAHRT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2):
                if BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3,4,5])
                    rand=5
                    print "z683"
                    print "rand =",rand
                    if rand==1:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                    elif rand==3:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==4:
                        BR130.startUmfahren(pause)
                    else:
                        ICE.startGleiswechsel(4,pause)
                elif BR130.stat(ANKUPPELN,RECHTS,4) and ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif BR130.stat(BEREIT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3,4])
                    rand=2
                    print "z713"
                    print "rand =",rand
                    if rand==1:
                        BR86.startAusfahrt(3, pause)
                        BR130.startAusfahrt(1,pause+4)
                    elif rand==2:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(4,pause)
                    else:
                        ICE.startGleiswechsel(4,pause)
                elif BR130.stat(UMFAHREN,RECHTS,4) and ICE.stat(BEREIT,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(ABKUPPELN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4,5,6])
                rand=4
                print "z675"
                print "rand =",rand
                if rand==1:
                    BR110.startAusfahrt(1,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==2:
                    BR110.startAusfahrt(4,pause)
                elif rand==3:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR118.startAbkuppeln(pause)
                elif rand==5:
                    BR130.startUmfahren(pause)
                else:
                    ICE.startGleiswechsel(4,pause)
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                rand=3
                print "z734"
                print "rand =",rand                
                if rand==1:
                    BR110.startGleiswechsel(4,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(4,pause+13)
                elif rand==4:
                    BR130.startUmfahren(pause)
                else:
                    ICE.startAusfahrt(4,pause)
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5,6])
                rand=3
                print "z696"
                print "rand =",rand                
                if rand==1:
                    BR110.startGleiswechsel(4,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(4,pause+13)
                elif rand==4:
                    BR118.startAbkuppeln(pause)
                elif rand==5:
                    BR130.startUmfahren(pause)
                else:
                    ICE.startAusfahrt(4,pause)
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            rand=random.choice([1,2])
            rand=2
            print "z569"
            print "rand =",rand
            if rand==1:
                BR86.startAusfahrt(2, pause)
                BR110.startAusfahrt(1,pause+4)
            elif rand==2:
                BR86.startAusfahrt(2, pause)
                BR110.startAusfahrt(2,pause)
            elif rand==3:
                BR86.startGleiswechsel(2,pause)
            elif rand==4:
                BR110.startAusfahrt(2,pause)
            else:
                ICE.startAusfahrt(2, pause)
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5])
                    rand=3
                    print "z791"
                    print "rand =",rand
                    if rand==1:
                        BR110.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause+13)
                    elif rand==4:
                        BR118.startUmfahren(pause)
                    else:
                        ICE.startAusfahrt(1,pause)
                elif ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3])
                    rand=3
                    print "z808"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(2,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2,pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5])
                    rand=3
                    print "z733"
                    print "rand =",rand
                    if rand==1:
                        BR110.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause+13)
                    elif rand==4:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(1,pause)
                elif ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3,4])
                    rand=3
                    print "z692"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(2,pause)
                    elif rand==2:
                        BR110.startAusfahrt(2,pause)
                    elif rand==3:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,1):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                else:
                    err()            
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                else:
                    err()            
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            else:
                err()        
        elif BR110.stat(EINFAHRT,RECHTS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                else:
                    err()
            else:
                err()        
        elif BR110.stat(GLEISWECHSEL,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,4) :
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()        
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()        
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                else:
                    err()
            else:
                err()        
        elif BR110.stat(NACH_RECHTS,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.nachGleis=2
            start_new_thread(BR86.gleiswechsel, (pause,))                
        else:
            err()
    elif BR86.stat(BEREIT,LINKS,2):
        if BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3])
                rand=2
                print "z979"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(1,pause)
                elif rand==2:
                    BR110.startAusfahrt(1,pause)
                else:
                    ICE.startAusfahrt(1,pause)
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4])
                rand=2
                print "z712"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(1,pause)
                elif rand==2:
                    BR110.startAusfahrt(1,pause)
                elif rand==3:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(1,pause)
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.status=AUSFAHRT
            BR86.nachGleis=2
            start_new_thread(BR86.ausfahrt, (pause,))                
        else:
            err()
    
    elif BR86.stat(BEREIT,RECHTS,1):
        if BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                rand=random.choice([1,2,3,4,5])
                rand=2
                print "z687"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                else:
                    ICE.startGleiswechsel(2,pause)
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                rand=random.choice([1,2,3,4,5,6])
                rand=2
                print "z686"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==5:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startGleiswechsel(2,pause)
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                rand=2
                print "z706"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startGleiswechsel(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(4,pause)
                else:
                    ICE.startAusfahrt(2,pause)
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5,6])
                rand=2
                print "z705"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startGleiswechsel(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(4,pause)
                elif rand==5:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(2,pause)
            else:
                err()        
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.nachGleis=3
            start_new_thread(BR86.gleiswechsel, (pause,))                
        else:
            err()
    elif BR86.stat(BEREIT,RECHTS,2):
        if BR110.stat(AUSFAHRT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,3):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3,4,5])
                    rand=5
                    print "z775"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                    elif rand==3:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    else:
                        ICE.startGleiswechsel(4,pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3,4,5])
                    rand=4
                    print "z794"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startAusfahrt(1,pause)
                    elif rand==3:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    else:
                        ICE.startGleiswechsel(1,pause)
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,3):
                        rand=random.choice([1,2,3,4,5])
                        rand=1
                        print "z704"
                        print "rand =",rand
                        if rand==1:
                            BR86.startGleiswechsel(4, pause)
                        elif rand==2:
                            BR110.startAusfahrt(4,pause)
                        elif rand==3:
                            BR110.startAusfahrt(3,pause)
                            ICE.startAusfahrt(2,pause+13)
                        elif rand==4:                        
                            BR110.startAusfahrt(4,pause)
                            ICE.startAusfahrt(2,pause+13)
                        else:
                            ICE.startAusfahrt(4,pause)
                    elif ICE.stat(BEREIT,RECHTS,4):
                        rand=random.choice([1,2,3,4,5])
                        if rand==1:
                            BR86.startGleiswechsel(3, pause)
                        elif rand==2:
                            BR110.startAusfahrt(3,pause)
                        elif rand==3:
                            BR110.startAusfahrt(3,pause)
                            ICE.startAusfahrt(2,pause+13)
                        elif rand==4:
                            BR110.startAusfahrt(4,pause)
                            ICE.startAusfahrt(2,pause+13)
                        else:
                            ICE.startAusfahrt(3,pause)
                    elif ICE.stat(GLEISWECHSEL,RECHTS,3):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,4):
                        reset()
                    else:
                        err()
                    
                elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3,4,5,6])
                    rand=1
                    print "z742"
                    print "rand =",rand
                    if rand==1:
                        BR86.nachGleis=3
                        start_new_thread(BR86.gleiswechsel, (pause,))
                    elif rand==2:
                        BR110.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                    elif rand==3:
                        BR110.nachGleis=3
                        ICE.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==4:
                        BR110.nachGleis=4
                        ICE.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==5:
                        start_new_thread(BR130.abkuppeln, (pause,))
                    else:
                        ICE.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause,))
                elif BR130.stat(ABKUPPELN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                    reset()
                else:
                    err()
            if BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3,4,5,6])
                    rand=5
                    print "z821"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR110.startAusfahrt(4,pause)
                    elif rand==3:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==5:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startGleiswechsel(4,pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3,4,5,6])
                    rand=5
                    print "z772"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startAusfahrt(1,pause)
                    elif rand==3:
                        BR110.startAusfahrt(1,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(4,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==5:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startGleiswechsel(1,pause)
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6])
                    rand=5
                    print "z889"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR110.startGleiswechsel(4,pause)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause)
                    elif rand==5:
                        BR130.startUmfahren(pause)
                    else:
                        ICE.ausfahrt(4,pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3])
                    rand=2
                    print "z908"
                    print "rand =",rand
                    if rand==1:
                        BR110.startAusfahrt(2,pause)
                    elif rand==2:
                        BR118.startUmfahren(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6,7])
                    rand=5
                    print "z824"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR110.startGleiswechsel(4,pause)
                    elif rand==3:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause)
                    elif rand==5:
                        BR118.startAbkuppeln(pause)
                    elif rand==6:
                        BR130.startUmfahren(pause)
                    else:
                        ICE.ausfahrt(4,pause)
                elif ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3])
                    rand=2
                    print "z818"
                    print "rand =",rand
                    if rand==1:
                        BR110.startAusfahrt(2,pause)
                    elif rand==2:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(BEREIT,RECHTS,4):
                    rand=random.choice([1,2,3])
                    if rand==1:
                        BR110.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                    elif rand==2:
                        start_new_thread(BR130.abkuppeln, (pause,))
                    else:
                        ICE.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause,))
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR130.stat(BEREIT,LINKS,1):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6,7])
                    rand=2
                    print "z357"                    
                    print "rand:",rand
                    if rand==1:
                        BR86.nachGleis=4
                        start_new_thread(BR86.gleiswechsel, (pause,))
                    elif rand==2:
                        BR86.nachGleis=1
                        BR130.nachGleis=2
                        start_new_thread(BR86.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt,(pause,))
                    elif rand==3:
                        BR110.nachGleis=4
                        start_new_thread(BR110.gleiswechsel, (pause,))
                    elif rand==4:
                        BR110.nachGleis=1
                        BR130.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==5:
                        BR110.nachGleis=2
                        ICE.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==6:
                        BR110.nachGleis=2
                        ICE.nachGleis=4
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    else:
                        ICE.nachGleis=4
                        start_new_thread(ICE.ausfahrt, (pause,))
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABKUPPELN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5])                    
                    print "Zufall 963"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startGleiswechsel(1,pause)
                    elif rand==3:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(4,pause+13)
                    else:
                        ICE.startAusfahrt(1,pause)
                elif ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3])
                    rand=3
                    print "z980"
                    print "rand =",rand
                    if rand==1:
                        BR110.startAusfahrt(2,pause)
                    elif rand==2:
                        BR118.startUmfahren(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(ANKUPPELN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(BEREIT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4])
                rand=1
                print "z1124"
                print "rand =",rand
                if rand==1:
                    BR86.startAusfahrt(1,pause)
                    BR118.startAusfahrt(2,pause+4)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR118.startGleiswechsel(2,pause)
                else:
                    ICE.startAusfahrt(2,pause)
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6])
                    rand=5
                    print "z915"
                    print "rand =",rand
                    if rand==1:
                        BR86.startGleiswechsel(1,pause)
                    elif rand==2:
                        BR110.startGleiswechsel(1,pause)
                    elif rand==3:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(1,pause+13)
                    elif rand==4:
                        BR110.startAusfahrt(2, pause)
                        ICE.startAusfahrt(4,pause+13)
                    elif rand==5:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(1,pause)
                elif ICE.stat(BEREIT,RECHTS,1):
                    rand=random.choice([1,2,3])
                    rand=2
                    print "z977"
                    print "rand =",rand
                    if rand==1:
                        BR110.startAusfahrt(2,pause)
                    elif rand==2:
                        BR118.startAbkuppeln(pause)
                    else:
                        ICE.startAusfahrt(2,pause)
                else:
                    err()
            elif BR118.stat(UMFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()


        elif BR110.stat(EINFAHRT,LINKS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,3) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(EINFAHRT,LINKS,4):
            if  BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            elif  BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(EINFAHRT,RECHTS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(NACH_RECHTS,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,3):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,3):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,4):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
                
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.status=GLEISWECHSEL
            BR86.nachGleis=1
            start_new_thread(BR86.gleiswechsel, (pause,))                
        else:
            err()
    elif BR86.stat(BEREIT,RECHTS,3):
        if BR110.stat(AUSFAHRT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()                
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4,5,6])
                rand=5
                print "z1780"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(4,pause)
                elif rand==2:
                    BR110.startAusfahrt(1,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                elif rand==5:
                    BR130.startAbkuppeln(pause)
                else:
                    ICE.startGleiswechsel(4)
                    
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABKUPPELN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):
                        rand=random.choice([1,2,3,4,5,6])
                        if rand==1:
                            BR86.nachGleis=4
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=4
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=4
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        else:
                            ICE.nachGleis=4
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(BEREIT,RECHTS,4):
                        rand=random.choice([1,2,3,4,5,6])
                        if rand==1:
                            BR86.nachGleis=2
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=4
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            BR118.nachGleis=2
                            start_new_thread(BR118.gleiswechsel, (pause,))
                        else:
                            ICE.nachGleis=2
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(GLEISWECHSEL,RECHTS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,4):
                        reset()
                    else:
                        err()
                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):
                        rand=random.choice([1,2,3,4,5,6,7])
                        if rand==1:
                            BR86.nachGleis=4
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=4
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=4
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        else:
                            ICE.nachGleis=4
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(BEREIT,RECHTS,4):
                        rand=random.choice([1,2,3,4,5,6])
                        if rand==1:
                            BR86.nachGleis=2
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=4
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            BR118.nachGleis=2
                            start_new_thread(BR118.gleiswechsel, (pause,))
                        elif rand==6:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        else:
                            ICE.nachGleis=2
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(GLEISWECHSEL,RECHTS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,4):
                        reset()
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT, RECHTS,1) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            rand=random.choice([1,2,3,4,5,6])
            rand=3
            print "z1922"
            print "rand =",rand
            if rand==1:
                BR86.startGleiswechsel(4,pause)
            elif rand==2:
                BR110.startAusfahrt(2,pause)
                ICE.startAusfahrt(1,pause+13)
            elif rand==3:
                BR110.startAusfahrt(2,pause)
                ICE.startAusfahrt(4,pause+13)
            elif rand==4:
                BR110.startGleiswechsel(4,pause)
            elif rand==5:
                BR130.startAbkuppeln(pause)
            else:
                ICE.startAusfahrt(4,pause)
        elif BR110.stat(BEREIT, RECHTS, 2):
            if BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6,7])
                    rand=1
                    print "z544"
                    print "rand:",rand
                    if rand==1:
                        BR86.startGleiswechsel(4,pause)
                    elif rand==2:
                        BR86.startAusfahrt(1,pause)
                        BR130.startAusfahrt(3,pause)
                    elif rand==3:
                        BR110.startGleiswechsel(4,pause)
                    elif rand==4:
                        BR110.startAusfahrt(1,pause)
                        BR130.startAusfahrt(2,pause)
                    elif rand==5:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(2,pause+13)
                    elif rand==6:
                        BR110.startAusfahrt(2,pause)
                        ICE.startAusfahrt(4,pause+13)
                    else:
                        ICE.startAusfahrt(4,pause)
                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(AUSFAHRT,LINKS,2):
                        reset()
                    elif (ICE.stat(BEREIT,LINKS,2)):
                        rand=random.choice([1,2,3,4,5])
                        if rand==1:
                            BR86.nachGleis=4
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=4
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            start_new_thread(BR118.abkuppeln, (pause,))
                        elif rand==5:
                            ICE.nachGleis=4
                            start_new_thread(ICE.ausfahrt, (pause,))
                    elif ICE.stat(BEREIT,RECHTS,4):
                        rand=random.choice([1,2,3])
                        if rand==1:
                            BR110.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==2:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        else:
                            ICE.nachGleis=2
                            start_new_thread(ICE.ausfahrt, (pause,))    
                    elif ICE.stat(EINFAHRT,RECHTS,2):
                        reset()
                    elif ICE.stat(NACH_RECHTS,LINKS,2):
                        reset()
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            rand=random.choice([1,2,3])
            rand=2
            print "z2013"
            print "rand =",rand
            if rand==1:
                BR110.startAusfahrt(2,pause)
            elif rand==2:
                BR130.startAbkuppeln(pause)
            else:
                ICE.startAusfahrt(2,pause)                
        elif BR110.stat(EINFAHRT,LINKS,1) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
            if ICE.stat(EINFAHRT,RECHTS,2):
                reset()
            elif ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(EINFAHRT,LINKS,4) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(EINFAHRT,RECHTS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                else:
                    err()                
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(NACH_LINKS,RECHTS,2):
                reset()
            else:
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,1) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
            if ICE.stat(AUSFAHRT,LINKS,2):
                reset()
            elif ICE.stat(EINFAHRT,RECHTS,2):
                reset()
            elif ICE.stat(EINGEFAHREN,RECHTS,1):
                reset()
            elif ICE.stat(NACH_RECHTS,LINKS,2):
                reset()
            else: 
                err()
        elif BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif  BR110.stat(NACH_LINKS,RECHTS,4) and  BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and    ICE.stat(BEREIT,RECHTS,1):
            reset()           
        elif BR110.stat(NACH_RECHTS,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(EINGEFAHREN,LINKS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                if ICE.stat(NACH_LINKS,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.status=GLEISWECHSEL
            BR86.nachGleis=4
            start_new_thread(BR86.gleiswechsel, (pause,))                
        else:
            err()
    elif BR86.stat(BEREIT,RECHTS,4):
        if BR110.stat(AUSFAHRT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(NACH_LINKS,RECHTS,2):
                reset()
            else:
                err()            
        elif BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4,5])
                rand=2
                print "z1476"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(1,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                else:
                    ICE.startGleiswechsel(2,pause)                
            elif BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4,5,6])
                rand=3
                print "z2022"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(3,pause)
                elif rand==2:
                    BR110.startAusfahrt(1,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(3,pause)
                elif rand==4:
                    BR110.startAusfahrt(3,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==5:
                    BR130.startAbkuppeln(pause)
                else:
                    ICE.startGleiswechsel(4,pause)                                                                                                                                                                
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):                
                        rand=random.choice([1,2,3,4,5])
                        if rand==1:
                            BR86.nachGleis=3
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=3
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=3
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        else:
                            ICE.nachGleis=3
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(BEREIT,RECHTS,3):
                        rand=random.choice([1,2,3,4,5,6])
                        if rand==1:
                            BR86.nachGleis=2
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=3
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            BR118.nachGleis=2
                            start_new_thread(BR118.gleiswechsel, (pause,))            
                        else:
                            ICE.nachGleis=2
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(GLEISWECHSEL,RECHTS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,3):
                        reset()
                    else:
                        err()

                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):
                        rand=random.choice([1,2,3,4,5,6])
                        rand=1
                        print "z1316"
                        print "rand =",rand
                        if rand==1:
                            BR86.nachGleis=3
                            start_new_thread(BR86.gleiswechsel, (pause,))
                        elif rand==2:
                            BR110.nachGleis=3
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=3
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        else:
                            ICE.nachGleis=3
                            start_new_thread(ICE.gleiswechsel, (pause,))
                    elif ICE.stat(GLEISWECHSEL,RECHTS,2):
                        reset()
                    else:
                        err()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                rand=random.choice([1,2,3,4,5,6])
                rand=2
                print "z1345"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(1,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(4,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==5:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startGleiswechsel(2,pause)                
                    
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                rand=2
                print "z1514"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startGleiswechsel(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2, pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                else:
                    ICE.startAusfahrt(2,pause)
            elif BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5])
                rand=2
                print "z2213"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(3,pause)
                elif rand==2:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==3:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(3,pause+13)
                elif rand==4:
                    BR130.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(3,pause)

            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5,6])
                rand=2
                print "z1265"
                print "rand =",rand
                if rand==1:
                    BR86.startGleiswechsel(2,pause)
                elif rand==2:
                    BR110.startGleiswechsel(2,pause)
                elif rand==3:
                    BR110.startAusfahrt(2, pause)
                    ICE.startAusfahrt(1,pause+13)
                elif rand==4:
                    BR110.startAusfahrt(2,pause)
                    ICE.startAusfahrt(2,pause+13)
                elif rand==5:
                    BR118.startAbkuppeln(pause)
                else:
                    ICE.startAusfahrt(2,pause)
            else:
                err()                                   
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                rand=random.choice([1,2,3,4,5,6,7,8,9])
                rand=2
                print "z695"
                print "rand:",rand
                if rand==1:
                    BR86.startGleiswechsel(3,pause)
                elif rand==2:
                    BR86.startAusfahrt(1,pause)
                    BR130.startAusfahrt(3,pause)
                elif rand==3:
                    BR110.nachGleis=3
                    start_new_thread(BR110.gleiswechsel, (pause,))
                elif rand==4:
                    BR110.nachGleis=1
                    BR130.nachGleis=2
                    start_new_thread(BR110.ausfahrt, (pause,))
                    start_new_thread(BR130.ausfahrt, (pause,))
                elif rand==5:
                    BR110.nachGleis=1
                    BR130.nachGleis=3
                    start_new_thread(BR110.ausfahrt, (pause,))
                    start_new_thread(BR130.ausfahrt, (pause,))
                elif rand==6:
                    BR110.nachGleis=2
                    ICE.nachGleis=2
                    start_new_thread(BR110.ausfahrt, (pause,))
                    start_new_thread(ICE.ausfahrt, (pause+13,))
                elif rand==7:
                    BR110.nachGleis=2
                    ICE.nachGleis=3
                    start_new_thread(BR110.ausfahrt, (pause,))
                    start_new_thread(ICE.ausfahrt, (pause+13,))
                elif rand==8:
                    BR118.nachGleis=1
                    BR130.nachGleis=3
                    start_new_thread(BR118.ausfahrt, (pause,))
                    start_new_thread(BR130.ausfahrt, (pause,))
                elif rand==9:
                    BR130.nachGleis=3
                    start_new_thread(BR130.ausfahrt, (pause,))
                else:
                    ICE.nachGleis=3
                    start_new_thread(ICE.ausfahrt, (pause,))
                    
                
                    
            elif BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6])
                    if rand==1:
                        BR86.nachGleis=3
                        start_new_thread(BR86.gleiswechsel, (pause,))
                    elif rand==2:
                        BR110.nachGleis=3
                        start_new_thread(BR110.gleiswechsel, (pause,))
                    elif rand==3:
                        BR110.nachGleis=2
                        ICE.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==4:
                        BR110.nachGleis=2
                        ICE.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==5:
                        start_new_thread(BR130.abkuppeln, (pause,))
                    else:
                        ICE.nachGleis=3
                        start_new_thread(ICE.ausfahrt, (pause,))
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        
        
        
        
        elif BR110.stat(BEREIT,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                rand=random.choice([1,2,3])
                if rand==1:
                    BR110.nachGleis=2
                    start_new_thread(BR110.ausfahrt, (pause,))
                elif rand==2:
                    ICE.nachGleis=2
                    start_new_thread(ICE.ausfahrt, (pause,))
                else:
                    start_new_thread(BR130.umfahren, (pause,))
            elif BR130.stat(ABKUPPELN,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                reset()
            elif BR130.stat(ANKUPPELN,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                reset()
            elif BR130.stat(BEREIT,LINKS,1):
                if ICE.stat(AUSFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(BEREIT,LINKS,2):
                    rand=random.choice([1,2,3,4,5,6,7,8,9,10])
                    rand=3
                    print "z744"
                    print "rand:",rand
                    if rand==1:
                        BR86.nachGleis=2
                        start_new_thread(BR86.gleiswechsel, (pause,))
                    elif rand==2:
                        BR110.nachGleis=2
                        start_new_thread(BR110.gleiswechsel, (pause,))
                    elif rand==3:
                        BR110.nachGleis=1
                        BR130.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==4:
                        BR110.nachGleis=1
                        BR130.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==5:
                        BR110.nachGleis=2
                        ICE.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==6:
                        BR110.nachGleis=2
                        ICE.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(ICE.ausfahrt, (pause+13,))
                    elif rand==7:
                        BR118.nachGleis=2
                        start_new_thread(BR118.gleiswechsel, (pause,))
                    elif rand==8:
                        BR118.nachGleis=1
                        BR130.nachGleis=2
                        start_new_thread(BR118.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==9:
                        BR130.nachGleis=2
                        start_new_thread(BR130.ausfahrt, (pause,))
                    else:
                        ICE.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause,))
                    
                elif ICE.stat(BEREIT,RECHTS,2):
                    rand=random.choice([1,2,3,4,5,6])
                    if rand==1:
                        BR110.nachGleis=1
                        BR130.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==2:
                        BR110.nachGleis=2
                        BR130.nachGleis=3
                        start_new_thread(BR110.ausfahrt, (pause,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==3:
                        BR110.nachGleis=2
                        start_new_thread(BR110.ausfahrt, (pause,))
                    elif rand==4:
                        ICE.nachGleis=1
                        BR130.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause+10,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    elif rand==5:
                        ICE.nachGleis=2
                        BR130.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause+10,))
                        start_new_thread(BR130.ausfahrt, (pause,))
                    else:
                        ICE.nachGleis=2
                        start_new_thread(ICE.ausfahrt, (pause,))
                elif ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,2):
                    reset()
                elif ICE.stat(NACH_RECHTS,LINKS,2):
                    reset()
                else:
                    err()
            elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                rand=random.choice([1,2,3])
                if rand==1:
                    BR110.nachGleis=2
                    start_new_thread(BR110.ausfahrt, (pause,))
                elif rand==2:
                    ICE.nachGleis=2
                    start_new_thread(ICE.ausfahrt, (pause,))
                else:
                    start_new_thread(BR130.abkuppeln, (pause,))
            elif BR130.stat(UMFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                reset()
            else:
                err()
        elif BR110.stat(EINFAHRT,RECHTS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,LINKS,1):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,2):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(GLEISWECHSEL,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        elif BR110.stat(NACH_RECHTS,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1):
                if ICE.stat(BEREIT,LINKS,2):
                    reset()
                elif ICE.stat(EINFAHRT,LINKS,1):
                    reset()
                elif ICE.stat(NACH_LINKS,RECHTS,1):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(EINFAHRT,LINKS,2):
                        reset()
                    elif ICE.stat(NACH_LINKS,RECHTS,2):
                        reset()
                    else:
                        err()
                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(NACH_LINKS,RECHTS,2):
                        reset()
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            BR86.status=AUSFAHRT
            BR86.nachGleis=1
            start_new_thread(BR86.ausfahrt, (pause,))                
        else:
            err()

    elif BR86.stat(EINFAHRT,LINKS,1):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(EINFAHRT,LINKS,2):
        if BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(EINFAHRT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(EINFAHRT,LINKS,3):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(EINFAHRT,LINKS,4):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINFAHRT,RECHTS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()

    elif BR86.stat(EINFAHRT,RECHTS,1):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2):
            if BR130.stat(EINFAHRT,LINKS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR130.stat(NACH_LINKS,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(EINFAHRT,RECHTS,2):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()

    elif BR86.stat(EINGEFAHREN,LINKS,1):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
            rand=random.choice([1,2,3,4,5,6])
            rand=2
            print "z990"
            print "rand = ",rand
            if rand==1:
                BR86.startAbkuppeln(pause)
            elif rand==2:
                BR110.startGleiswechsel(4,pause)
            elif rand==3:
                BR110.startAusfahrt(2, pause)
                ICE.startAusfahrt(2,pause+13)
            elif rand==4:
                BR110.startAusfahrt(2, pause)
                ICE.startAusfahrt(4,pause+13)                
            elif rand==5:
                BR130.startAbkuppeln(pause)
            else:
                ICE.startAusfahrt(4,pause)
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
            rand=random.choice([1,2,3,4])
            rand=2
            print "z2055"
            print "rand =",rand
            if rand==1:
                BR86.startAbkuppeln(pause)
            elif rand==2:
                BR110.startAusfahrt(2,pause)
            elif rand==3:
                BR118.startAbkuppeln(pause)
            else:
                ICE.startAusfahrt(2,pause)
                
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            start_new_thread(BR86.abkuppeln, (pause,))
        else:
            err()

    elif BR86.stat(EINGEFAHREN,RECHTS,2):
        if BR110.stat(BEREIT,LINKS,1) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            rand=random.choice([1,2,3,4,5,6])
            rand=2
            print "z1380"
            print "rand =",rand
            if rand==1:
                BR86.startAbkuppeln(pause)
            elif rand==2:
                BR110.startGleiswechsel(pause)
            elif rand==3:
                BR110.startAusfahrt(1,pause)
                BR118.startAusfahrt(1, pause+5)
            elif rand==4:
                BR110.startAusfahrt(4,pause)
                ICE.startAusfahrt(1,pause+13)
            elif rand==5:
                BR110.startAusfahrt(4,pause)
                ICE.startAusfahrt(2,pause+13)
            else:
                ICE.startAusfahrt(2,pause)
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            start_new_thread(BR86.abkuppeln, (pause,))
        else:
            err()
    elif BR86.stat(EINGEFAHREN,RECHTS,3):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            rand=random.choice([1,2,3,4,5])
            rand=1
            print "z2486"
            print "rand =",rand
            if rand==1:
                BR86.startAbkuppeln(pause)
            elif rand==2:
                BR110.startAusfahrt(1,pause)
                ICE.startAusfahrt(2,pause+13)
            elif rand==3:
                BR110.startAusfahrt(4,pause)
            elif rand==4:
                BR130.startAbkuppeln(pause)
            else:
                ICE.startGleiswechsel(4,pause)
            
        elif BR110.stat(BEREIT,RECHTS,4):
            if (BR118.stat(BEREIT,RECHTS,1)):
                if BR130.stat(ABKUPPELN,LINKS,1):
                    if (ICE.stat(BEREIT,RECHTS,2)):
                        reset()
                    else:
                        err()
                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if (ICE.stat(AUSFAHRT,LINKS,2)):
                        reset()
                    elif (ICE.stat(BEREIT,LINKS,2)):
                        rand=random.choice([1,2,3,4,5,6])
                        if rand==1:
                            start_new_thread(BR86.abkuppeln, (pause,))
                        elif rand==2:
                            BR110.nachGleis=2
                            start_new_thread(BR110.gleiswechsel, (pause,))
                        elif rand==3:
                            BR110.nachGleis=2
                            ICE.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==4:
                            BR110.nachGleis=2
                            ICE.nachGleis=4
                            start_new_thread(BR110.ausfahrt, (pause,))
                            start_new_thread(ICE.ausfahrt, (pause+13,))
                        elif rand==5:
                            BR118.nachGleis=2
                            start_new_thread(BR118.gleiswechsel, (pause,))
                        elif rand==6:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        elif rand==7:
                            ICE.nachGleis=2
                            start_new_thread(ICE.ausfahrt, (pause,))
                    elif (ICE.stat(BEREIT,RECHTS,2)):
                        rand=random.choice([1,2,3,4])
                        if rand==1:
                            start_new_thread(BR86.abkuppeln, (pause,))                    
                        elif rand==2:
                            BR110.nachGleis=2
                            start_new_thread(BR110.ausfahrt, (pause,))
                        elif rand==3:
                            start_new_thread(BR130.abkuppeln, (pause,))
                        elif rand==4:
                            ICE.nachGleis=2
                            start_new_thread(ICE.ausfahrt, (pause,))
                        else:
                            err()
                    elif (ICE.stat(EINFAHRT,LINKS,1)):
                        reset()
                    elif (ICE.stat(EINFAHRT,LINKS,2)):
                        reset()
                    elif (ICE.stat(EINFAHRT,LINKS,3)):
                        reset()
                    elif (ICE.stat(EINFAHRT,LINKS,4)):
                        reset()
                    elif (ICE.stat(EINFAHRT,RECHTS,1)):
                        reset()
                    elif (ICE.stat(EINFAHRT,RECHTS,2)):
                        reset()
                    elif (ICE.stat(NACH_LINKS,RECHTS,1)):
                        reset()
                    elif (ICE.stat(NACH_LINKS,RECHTS,2)):
                        reset()
                    elif (ICE.stat(NACH_LINKS,RECHTS,3)):
                        reset()
                    elif (ICE.stat(NACH_LINKS,RECHTS,4)):
                        reset()
                    elif (ICE.stat(NACH_RECHTS,LINKS,1)):
                        reset()
                    elif (ICE.stat(NACH_RECHTS,LINKS,2)):
                        reset()
                    else:
                        err()
                else:
                    err()
            else:                
                err()                        
        else:
            err()
    elif BR86.stat(GLEISWECHSEL,LINKS,1):
        if BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()                

        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(GLEISWECHSEL,LINKS,2):
        if BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            

    elif BR86.stat(GLEISWECHSEL,RECHTS,1):
        if BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
                reset()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(GLEISWECHSEL,RECHTS,2):
        if BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,3):
                        reset()
                    elif ICE.stat(BEREIT,RECHTS,4):
                        reset()
                    else:
                        err()
                elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3):
                if ICE.stat(BEREIT,RECHTS,1):
                    reset()
                elif ICE.stat(BEREIT,RECHTS,4):
                    reset()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        elif BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(GLEISWECHSEL,RECHTS,3):
        if BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                    reset()
                elif BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(BEREIT,RECHTS,4):
                    reset()
                elif BR130.stat(EINGEFAHREN,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):                
                        reset()
                    elif ICE.stat(BEREIT,RECHTS,4):                
                        reset()
                    else:
                        err()
                else:
                    err()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT, LINKS,2):
            reset()
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(GLEISWECHSEL,RECHTS,4):
        if BR110.stat(BEREIT,LINKS,2):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(BEREIT,RECHTS,1):
                if BR130.stat(ABGEKUPPELT,LINKS,1):
                    if ICE.stat(BEREIT,RECHTS,2):
                        reset()
                    elif ICE.stat(BEREIT,RECHTS,3):
                        reset()
                    else:
                        err()
                elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,2):
                    reset()
                else:
                    err()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,1):
            if BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()            
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):
            if BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(BEREIT,RECHTS,3) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(BEREIT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            

    elif BR86.stat(NACH_LINKS,RECHTS,1):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(NACH_LINKS,RECHTS,2):
        if BR110.stat(BEREIT,RECHTS,4):
            if BR118.stat(AUSFAHRT,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINFAHRT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR118.stat(NACH_RECHTS,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(NACH_LINKS,RECHTS,3):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(NACH_LINKS,RECHTS,4):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1):            
            if BR130.stat(AUSFAHRT,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(BEREIT,RECHTS,3) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(EINFAHRT,RECHTS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            elif BR130.stat(NACH_RECHTS,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
                reset()
            else:
                err()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    
    elif BR86.stat(NACH_RECHTS,LINKS,1):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2):
            if BR130.stat(EINFAHRT,LINKS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            elif BR130.stat(NACH_LINKS,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
                reset()
            else:
                err()
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
    elif BR86.stat(NACH_RECHTS,LINKS,2):
        if BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()            
############################# BR 110

    elif BR86.stat(PARKED):
        if BR110.stat(AUSFAHRT,LINKS,1) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        elif BR110.stat(AUSFAHRT,LINKS,2) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        elif BR110.stat(BEREIT,LINKS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startGleiswechsel(2,pause)
        elif BR110.stat(BEREIT,LINKS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startAusfahrt(1,pause)
        elif BR110.stat(BEREIT,RECHTS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startGleiswechsel(2,pause)
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startAusfahrt(1,pause)
        elif BR110.stat(BEREIT,RECHTS,3) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startGleiswechsel(4,pause)
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(PARKED) and BR130.stat(PARKED):
            BR110.startGleiswechsel(1,pause)    
        elif BR110.stat(EINFAHRT,LINKS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(EINFAHRT,LINKS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(EINFAHRT,LINKS,3) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(EINFAHRT,LINKS,4) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(EINFAHRT,RECHTS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(EINFAHRT,RECHTS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,LINKS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,LINKS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,RECHTS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,RECHTS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,RECHTS,3) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(GLEISWECHSEL,RECHTS,4) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,3) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_LINKS,RECHTS,4) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_RECHTS,LINKS,1) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()
        elif BR110.stat(NACH_RECHTS,LINKS,2) and BR118.stat(PARKED) and BR130.stat(PARKED):
            reset()

############################# BR 118
        
        elif BR110.stat(PARKED):
            if BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=UMFAHREN
                start_new_thread(BR118.umfahren, (pause,))
        
            elif BR118.stat(ABGEKUPPELT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=UMFAHREN
                start_new_thread(BR118.umfahren, (pause,))
        
            elif BR118.stat(ABKUPPELN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                    reset()
            elif BR118.stat(ABKUPPELN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(ANKUPPELN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
        
            elif BR118.stat(ANKUPPELN,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()

            elif BR118.stat(AUSFAHRT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(AUSFAHRT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()

            elif BR118.stat(BEREIT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=GLEISWECHSEL
                BR118.nachGleis=2
                start_new_thread(BR118.gleiswechsel, (pause,))                
            elif BR118.stat(BEREIT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=AUSFAHRT
                BR118.nachGleis=2
                start_new_thread(BR118.ausfahrt, (pause,))
        
            elif BR118.stat(BEREIT,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=AUSFAHRT
                BR118.nachGleis=1
                start_new_thread(BR118.ausfahrt, (pause,))                
            elif BR118.stat(BEREIT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=GLEISWECHSEL
                BR118.nachGleis=1
                start_new_thread(BR118.gleiswechsel, (pause,))                
    
            elif BR118.stat(EINFAHRT,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(EINFAHRT,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(EINFAHRT,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(EINFAHRT,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
        
            elif BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=ABKUPPELN
                start_new_thread(BR118.abkuppeln, (pause,))

            elif BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                BR118.status=ABKUPPELN
                start_new_thread(BR118.abkuppeln, (pause,))

            elif BR118.stat(GLEISWECHSEL,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(GLEISWECHSEL,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(GLEISWECHSEL,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(GLEISWECHSEL,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()

            elif BR118.stat(NACH_LINKS,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(NACH_LINKS,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(NACH_RECHTS,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(NACH_RECHTS,LINKS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()

############################# BR 130

            elif BR118.stat(PARKED):
                if BR130.stat(ABGEKUPPELT,LINKS,1) and ICE.stat(PARKED):
                    BR130.status=UMFAHREN
                    start_new_thread(BR130.umfahren, (pause,))
    
                elif BR130.stat(ABGEKUPPELT,RECHTS,2) and ICE.stat(PARKED):
                    BR130.status=UMFAHREN
                    start_new_thread(BR130.umfahren, (pause,))

                elif BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(PARKED):
                    BR130.status=UMFAHREN
                    start_new_thread(BR130.umfahren, (pause,))
    
                elif BR130.stat(ABKUPPELN,LINKS,1) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(ABKUPPELN,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(ABKUPPELN,RECHTS,3) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(ANKUPPELN,LINKS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(ANKUPPELN,RECHTS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(ANKUPPELN,RECHTS,3) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(ANKUPPELN,RECHTS,4) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(AUSFAHRT,LINKS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(AUSFAHRT,LINKS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(AUSFAHRT,RECHTS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(AUSFAHRT,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(AUSFAHRT,RECHTS,3) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(AUSFAHRT,RECHTS,4) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(BEREIT,LINKS,1) and ICE.stat(PARKED):
                    BR130.status=GLEISWECHSEL
                    BR130.nachGleis=2
                    start_new_thread(BR130.gleiswechsel, (pause,))                
                elif BR130.stat(BEREIT,LINKS,2) and ICE.stat(PARKED):
                    BR130.status=AUSFAHRT
                    BR130.nachGleis=3
                    start_new_thread(BR130.ausfahrt, (pause,))                

                elif BR130.stat(BEREIT,RECHTS,1) and ICE.stat(PARKED):
                    BR130.status=GLEISWECHSEL
                    BR130.nachGleis=4
                    start_new_thread(BR130.gleiswechsel, (pause,))
                elif BR130.stat(BEREIT,RECHTS,2) and ICE.stat(PARKED):
                    BR130.status=AUSFAHRT
                    BR130.nachGleis=1
                    start_new_thread(BR130.ausfahrt, (pause,))                
                elif BR130.stat(BEREIT,RECHTS,3) and ICE.stat(PARKED):
                    BR130.status=GLEISWECHSEL
                    BR130.nachGleis=1
                    start_new_thread(BR130.gleiswechsel, (pause,))
                elif BR130.stat(BEREIT,RECHTS,4) and ICE.stat(PARKED):
                    BR130.status=GLEISWECHSEL
                    BR130.nachGleis=2
                    start_new_thread(BR130.gleiswechsel, (pause,))

                elif BR130.stat(EINFAHRT,RECHTS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(EINFAHRT,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(EINFAHRT,LINKS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(EINFAHRT,LINKS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(EINFAHRT,LINKS,3) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(EINFAHRT,LINKS,4) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(PARKED):
                    BR130.status=ABKUPPELN
                    start_new_thread(BR130.abkuppeln, (pause,))
    
                elif BR130.stat(EINGEFAHREN,RECHTS,2) and ICE.stat(PARKED):
                    BR130.status=ABKUPPELN
                    start_new_thread(BR130.abkuppeln, (pause,))
                elif BR130.stat(EINGEFAHREN,RECHTS,3) and ICE.stat(PARKED):
                    BR130.status=ABKUPPELN
                    start_new_thread(BR130.abkuppeln, (pause,))

                elif BR130.stat(GLEISWECHSEL,LINKS,1) and ICE.stat(PARKED):
                        reset()
                elif BR130.stat(GLEISWECHSEL,LINKS,2) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(GLEISWECHSEL,RECHTS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(GLEISWECHSEL,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(GLEISWECHSEL,RECHTS,3) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(GLEISWECHSEL,RECHTS,4) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_LINKS,RECHTS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_LINKS,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_LINKS,RECHTS,3) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_LINKS,RECHTS,4) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_RECHTS,LINKS,1) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(NACH_RECHTS,LINKS,2) and ICE.stat(PARKED):
                    reset()
        
###################################### BR ICE

                elif BR130.stat(PARKED):
                    if ICE.stat(AUSFAHRT,LINKS,1):
                            reset()
                    elif ICE.stat(AUSFAHRT,LINKS,2):
                        reset()
                    elif ICE.stat(BEREIT,LINKS,1):
                        ICE.status=GLEISWECHSEL
                        ICE.nachGleis=2
                        start_new_thread(ICE.gleiswechsel,(pause,))
                    elif ICE.stat(BEREIT,LINKS,2):
                        ICE.status=AUSFAHRT
                        ICE.nachGleis=2
                        start_new_thread(ICE.ausfahrt,(pause,))
        
                    elif ICE.stat(BEREIT,RECHTS,1):
                        ICE.status=AUSFAHRT
                        ICE.nachGleis=1
                        start_new_thread(ICE.ausfahrt,(pause,))
                    elif ICE.stat(BEREIT,RECHTS,2):
                        ICE.status=GLEISWECHSEL
                        ICE.nachGleis=3
                        start_new_thread(ICE.gleiswechsel,(pause,))
                    elif ICE.stat(BEREIT,RECHTS,3):
                        ICE.status=GLEISWECHSEL
                        ICE.nachGleis=4
                        start_new_thread(ICE.gleiswechsel,(pause,))
                    elif ICE.stat(BEREIT,RECHTS,4):
                        ICE.status=GLEISWECHSEL
                        ICE.nachGleis=1
                        start_new_thread(ICE.gleiswechsel,(pause,))
                    elif ICE.stat(EINFAHRT,LINKS,1):
                            reset()    
                    elif ICE.stat(EINFAHRT,LINKS,2):
                        reset()
                    elif ICE.stat(EINFAHRT,LINKS,3):
                        reset()
                    elif ICE.stat(EINFAHRT,LINKS,4):
                        reset()
                    elif ICE.stat(EINFAHRT,RECHTS,1):
                        reset()
                    elif ICE.stat(EINFAHRT,RECHTS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,LINKS,1):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,LINKS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,1):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,2):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,3):
                        reset()
                    elif ICE.stat(GLEISWECHSEL,RECHTS,4):
                        reset()
                    elif ICE.stat(NACH_LINKS,RECHTS,1):
                        reset()
                    elif ICE.stat(NACH_LINKS,RECHTS,2):
                        reset()
                    elif ICE.stat(NACH_LINKS,RECHTS,3):
                        reset()
                    elif ICE.stat(NACH_LINKS,RECHTS,4):
                        reset()
                    elif ICE.stat(NACH_RECHTS,LINKS,1):
                        reset()
                    elif ICE.stat(NACH_RECHTS,LINKS,2):
                        reset()
                    else:
                        err()
###################################### BR 86

                elif BR130.stat(UMFAHREN,LINKS,1) and ICE.stat(PARKED):
                    reset()

                elif BR130.stat(UMFAHREN,RECHTS,1) and ICE.stat(PARKED):
                    reset()    
                elif BR130.stat(UMFAHREN,RECHTS,2) and ICE.stat(PARKED):
                    reset()
                elif BR130.stat(UMFAHREN,RECHTS,3) and ICE.stat(PARKED):
                    reset()    
                elif BR130.stat(UMFAHREN,RECHTS,4) and ICE.stat(PARKED):
                    reset()
                else:
                    err()
###################################### BR118
        
            elif BR118.stat(UMFAHREN,LINKS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(UMFAHREN,RECHTS,1) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            elif BR118.stat(UMFAHREN,RECHTS,2) and BR130.stat(PARKED) and ICE.stat(PARKED):
                reset()
            else:
                err()
        else:
            err()
###################################### BR 86
    elif BR86.stat(UMFAHREN,LINKS,1):
        if BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(BEREIT,RECHTS,4) and BR118.stat(EINGEFAHREN,RECHTS,2) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(UMFAHREN,RECHTS,1):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(EINGEFAHREN,LINKS,1) and BR130.stat(ABGEKUPPELT,RECHTS,3) and ICE.stat(BEREIT,RECHTS,4):
            reset()
        elif BR110.stat(PARKED) and BR118.stat(PARKED) and BR130.stat(PARKED) and ICE.stat(PARKED):
            reset()
        else:
            err()
    elif BR86.stat(UMFAHREN,RECHTS,4):
        if BR110.stat(BEREIT,LINKS,2) and BR118.stat(ABGEKUPPELT,RECHTS,2) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,RECHTS,1):
            reset()
        elif BR110.stat(BEREIT,RECHTS,2) and BR118.stat(BEREIT,RECHTS,1) and BR130.stat(EINGEFAHREN,LINKS,1) and ICE.stat(BEREIT,LINKS,2):
            reset()
        else:
            err()
    else:        
        err()
    
    if (statecount>0):
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

#!/usr/bin/python
# coding=utf8

from train import *
from track import *
from mcp23s17 import *
import select,sys,termios,tty

try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

def triggerContacts(input):
    print input
    
def keyPressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

SRCP_BUS=1
commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

# Wagen

doppelstockeinheit_lang=Waggon(60)
doppelstockeinheit_kurz=Waggon(30)

# Züge

doppelstockzug_lang=[doppelstockeinheit_lang]
doppelstockzug_kurz=[doppelstockeinheit_kurz]

# Loks

ICE=Loco(SRCP_BUS,1,10,10) # Längen korrigieren
BR110=Loco(SRCP_BUS,2,5,5)

# Züge
BR110.appendA(doppelstockzug_lang)

# Gleise
track1=Track("Abstellbahnhof vorn/1")
track2=Track("Abstellbahnhof vorn/2")
track3=Track("Abstellbahnhof vorn/3")
track4=Track("Abstellbahnhof vorn/4")
track5=Track("Abstellbahnhof vorn/5")

track1.connectTo(track2)
track1.connectTo(track3)
track1.connectTo(track4)
track1.connectTo(track5)

track2.connectTo(track1)
track2.connectTo(track3)
track2.connectTo(track4)
track2.connectTo(track5)

track3.connectTo(track1)
track3.connectTo(track2)
track3.connectTo(track4)
track3.connectTo(track5)

track4.connectTo(track1)
track4.connectTo(track2)
track4.connectTo(track3)
track4.connectTo(track5)

track5.connectTo(track1)
track5.connectTo(track2)
track5.connectTo(track3)
track5.connectTo(track4)

###### MAIN ######

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

quit=False
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

    if quit:
        break        
    time.sleep(0.01)

commandbus.powerOff()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

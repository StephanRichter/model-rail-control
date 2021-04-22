#!/usr/bin/python
from classes.S88 import *

RESET=5
LOAD=7
CLOCK=11
DATA=13
CONTACTS=64

chips = S88(CONTACTS, DATA, CLOCK, RESET,LOAD)

old=0
while True:
    val = chips.readValue()
    diff=old^val

    for i in range(chips.contacts,0,-1):
        if 1<<i-1 & diff:
            if 1<<i-1 & val:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
            else:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";
            
            print msg
    old=val
    
    time.sleep(0.01)

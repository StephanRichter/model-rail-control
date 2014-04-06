#!/usr/bin/python
# coding=utf8
import socket,sys
from mcp23s17 import *

MCPs=(0,1)

activateAdressing()
for addr in MCPs:
    initMCP23S17(addr,0xFF,0xFF) # all-read 

old=0
while True:
    val=0
    for addr in (MCPs):
        val<<=8
        val = val|readSPI(addr, SPI_GPIOA)
        val<<=8
        val = val|readSPI(addr, SPI_GPIOB)

    diff=old^val

    for i in range(16*len(MCPs),0,-1):
        if 1<<i-1 & diff:
            if 1<<i-1 & val:
                msg=str(time.time())+" contact "+str(i)+" => 1";
            else:
                msg=str(time.time())+" contact "+str(i)+" => 0";
            
            print(msg,True)
    old=val
    
    time.sleep(0.01)

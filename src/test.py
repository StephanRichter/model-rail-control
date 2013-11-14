#!/usr/bin/python

import srcp
import time

SRCP_BUS=1
commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

ICE = srcp.GL(SRCP_BUS, 1)
ICE.init('N', '1', 128, 4)

ICE.setDirection(0)
ICE.setSpeed(50)
ICE.send()

time.sleep(5)
ICE.setSpeed(0)
ICE.send()
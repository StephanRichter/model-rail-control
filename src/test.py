#!/usr/bin/python

import srcp
import time

SRCP_BUS=1

ICE = srcp.GL(SRCP_BUS, 1)

ICE.setDirection(0)
ICE.setSpeed(100)
ICE.send()

time.sleep(5)
ICE.setSpeed(0)
ICE.send()
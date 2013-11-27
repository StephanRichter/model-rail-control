#!/usr/bin/python
# coding=utf8
import os
import random
from thread import start_new_thread
import time

from br110 import BR110
from br118 import BR118
from br130 import BR130
from br86 import BR86
from ice import ICE
from kontakte import *
from lok import *
from mcp23s17 import *


SRCP_BUS=1
commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

BR86 = BR86(srcp.GL(SRCP_BUS,3))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR130 = BR130(srcp.GL(SRCP_BUS,5))
ICE = ICE(srcp.GL(SRCP_BUS, 1))

tfz=ICE


tfz.nachLinks()
tfz.speed(50)

time.sleep(15)
tfz.stop()
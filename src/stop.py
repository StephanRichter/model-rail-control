from thread import start_new_thread
from train import Train
from ice import ICE
from br110 import BR110
from br86 import BR86
from br118 import BR118
from br130 import BR130
from mcp23s17 import *
import time,os


try:
    import srcp
except:
    print "%Can't connect to the srcp server!"
    print "Please start it before or check srcp.py config!"
    exit()

SRCP_BUS=1    

commandbus=srcp.BUS(SRCP_BUS);    
commandbus.powerOn()

ICE = ICE(srcp.GL(SRCP_BUS, 1))
BR110 = BR110(srcp.GL(SRCP_BUS,2))
BR86 = BR86(srcp.GL(SRCP_BUS, 3))
BR118 = BR118(srcp.GL(SRCP_BUS,4))
BR130 = BR130(srcp.GL(SRCP_BUS,5))
  
commandbus.powerOff()
BR118.stop()
ICE.stop()
BR110.stop()
BR86.stop()
BR118.stop()
BR130.stop()
os._exit(0)

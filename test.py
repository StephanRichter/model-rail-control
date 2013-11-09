#!/usr/bin/python

import srcp
import time

SRCP_BUS=1

Lok = srcp.GL(SRCP_BUS, 1)

Lok.setF(1,1)
Lok.send()

time.sleep(3)

Lok.setF(1,0)
Lok.send()


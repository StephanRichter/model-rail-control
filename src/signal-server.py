#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
from classes.SpiConnection import *
from classes.SRCPSock import *
from classes.RocrailProxy import *

if __name__ == "__main__":
    cable_select=7
    clock=11
    mosi=13
    miso=15
    
    conn = SpiConnection(cable_select,clock,mosi,miso)
    signalDriver = conn.signalDriver(2)
    signalDriver.assign(1,SignalDriver.RoGeGr)
    signalDriver.assign(2,SignalDriver.RoGeGr)
    signalDriver.assign(3,SignalDriver.RoGr)
    
    server = RocrailProxy('localhost',4305);    
    server.connectTo(signalDriver)

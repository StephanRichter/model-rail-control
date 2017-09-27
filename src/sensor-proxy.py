#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
from classes.SpiConnection import *
from classes.SRCPSock import *
from classes.RocrailProxy import *

if __name__ == "__main__":
    cable_select=12
    clock=16
    mosi=18
    miso=22
    
    locos=40
    accesoires=10

    conn = SpiConnection(cable_select,clock,mosi,miso)
    sensors=(conn.sensor(3),conn.sensor(0),conn.sensor(1),conn.sensor(2))
    srcpSock = SRCPSock('localhost',4303);
    srcpSock.setup(locos,accesoires)
    proxy = RocrailProxy('localhost',4304);
    proxy.addSensors(sensors)
    proxy.forward(srcpSock)
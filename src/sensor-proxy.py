#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
from classes.S88 import *
from classes.SRCPSock import *
from classes.RocrailProxy import *

if __name__ == "__main__":
    RESET=5
    LOAD=7
    CLOCK=11
    DATA=13
    CONTACTS=48
    
    locos=40
    accesoires=10

    sensors=S88(CONTACTS,DATA,CLOCK,RESET,LOAD)
    srcpSock = SRCPSock('localhost',4303);
    srcpSock.setup(locos,accesoires)
    proxy = RocrailProxy('192.168.1.225',4304);
    proxy.addSensors(sensors)
    proxy.forward(srcpSock)

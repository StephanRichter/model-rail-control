#!/usr/bin/python
# coding=utf8
import socket,sys,time;
from thread import *

try:
    srcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error, msg:
    print "Failed to create socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
    sys.exit();

print "socket created"

srcphost = 'localhost'
srcpport = 4303
try:
    srcpip=socket.gethostbyname(srcphost)
except:
    print "Hostname "+srcphost+" could not be resolved. Exiting"
    sys.exit()
    
print "Ip adress of "+srcphost+" is "+srcpip

srcpsock.connect((srcpip , srcpport))
 
print 'Socket Connected to ' + srcphost + ' on ip ' + srcpip

welcome = srcpsock.recv(1024)
print welcome

def send(msg):
    print "Sending "+msg
    try:
        srcpsock.sendall(msg+"\n")
    except socket.error:
        print 'Send failed'
        sys.exit()
    reply = srcpsock.recv(1024)
    print reply


send("SET PROTOCOL SRCP 0.8.4")
send("GO")
send("INIT 1 GA 1 N")
send("SET 1 POWER ON")
time.sleep(1)
send("SET 1 GA 1 0 1 100")
time.sleep(1)
send("SET 1 GA 1 1 1 100")
time.sleep(1)
srcpsock.close()
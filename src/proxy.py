#!/usr/bin/python
# coding=utf8
import socket,sys,time
from thread import start_new_thread
from mcp23s17 import *
from sys import exit


serverhost=''
serverport=4304

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendAndRcv(sock,message):
    print message
    sock.sendall(message+"\n")
    reply=sock.recv(1024)    
    print reply[:-1]

try:
    srcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error, msg:
    print "Failed to create socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
    sys.exit()

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

sendAndRcv(srcpsock,"SET PROTOCOL SRCP 0.8")
sendAndRcv(srcpsock,"SET CONNECTIONMODE SRCP COMMAND")
sendAndRcv(srcpsock, "GO")
sendAndRcv(srcpsock, "SET 1 POWER ON")
for addr in range(1,20):
    time.sleep(0.01)
    sendAndRcv(srcpsock, "INIT 1 GL "+str(addr)+" N 1 128 4")
    sendAndRcv(srcpsock, "INIT 1 GA "+str(addr)+" N")
sendAndRcv(srcpsock, "TERM 0 SESSION")
srcpsock.close()

print 'Socket created'
 
try:
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((serverhost, serverport))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

serversocket.listen(10)
print 'Socket now listening'

def prnt(text,info):
    if info:
        print "\033[1;40;31m"+text+"\033[0m"
    else:
        print text
        
def sensorThread(source,sink):
    bits=8    
    ledPattern = 0b00000000 # ideally this should adapt to the value of <bits>
    old=0
    while True:    
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
        val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
        diff=old^val
        for i in range(16,0,-1):
            if 1<<i-1 & diff:
                if 1<<i-1 & val:
                    msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
                else:
                    msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";

                prnt(msg,True)
                source.sendall(msg+"\n")
        old=val
        
        time.sleep(0.01)
        
def initialize(sink):
    for adress in range(1,20):
        command="INIT 1 GA "+str(adress)+" N"
        print command+" >>>"
        sink.sendall(command+"\n")
        response=sink.recv(1024)
        print "<<< "+response            
        
def connectA(source,sink,connection):
    while True:
        data=source.recv(1024)
        if not data:
            break
        prnt(data[:-1]+" >>>",infsession[connection])
        sink.sendall(data)
        if data=="SET CONNECTIONMODE SRCP INFO\n":
            infsession[connection]=True
            start_new_thread(sensorThread, (source,sink,))
    try:
        source.close()
    except:
        pass
    print "connection closed"    
    
def connectB(source,sink,connection):
    while True:
        data=source.recv(1024)
        if not data:
            break
        prnt("<<< "+data[:-1],infsession[connection]) 
        sink.sendall(data)
    try:
        source.close()
    except:
        pass
    print "connection closed"


def clientthread(client,connection):    
    try:
        srcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error, msg:
        print "Failed to create socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
        return()
    
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
    client.send(welcome)
    
    start_new_thread(connectA, (client,srcpsock,connection,))
    start_new_thread(connectB, (srcpsock,client,connection,))
    
####
    
connection=0
infsession=[]
                     
while 1:
    #wait to accept a connection - blocking call
    client, addr = serversocket.accept()
    infsession.append(False)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (client,connection,))
    connection+=1    
 
serversocket.close()
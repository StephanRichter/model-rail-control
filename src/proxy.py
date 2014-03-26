#!/usr/bin/python
# coding=utf8
import socket,sys,time
from thread import start_new_thread
from mcp23s17 import *


serverhost=''
serverport=4304

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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



#for style in xrange(8):
#        for fg in xrange(30,38):
#            s1 = ''
#            for bg in xrange(40,48):
#                format = ';'.join([str(style), str(fg), str(bg)])
#                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#            print s1
#        print '\n'
        
def prnt(text,info):
    if info:
        print "\033[1;40;31m"+text+"\033[0m"
    else:
        print text
        
def sensorThread(source,sink):
    ledPattern = 0b00000000
    while True:    
        sendSPI(SPI_SLAVE_ADDR, SPI_GPIOB, ledPattern)
        val = readSPI(SPI_SLAVE_ADDR, SPI_GPIOA)
        if val:
            for i in range(8):
                if val & (1<<i):
                    print i
#        msg=str(time.time())+" 100 INFO 0 FB 64 0";
#        print msg
#        source.sendall(msg+"\n")
        time.sleep(0.01)            
        
def connectA(source,sink,connection):
    while True:
        data=source.recv(1024)
        if not data:
            break
        prnt(data[:-1]+" >>>",infsession[connection])
        if data=="SET CONNECTIONMODE SRCP INFO\n":
            infsession[connection]=True
            start_new_thread(sensorThread, (source,sink,)) 
        sink.sendall(data)
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
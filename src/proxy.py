#!/usr/bin/python
# coding=utf8
import socket,sys,time
from thread import start_new_thread
from time import gmtime, clock


serverhost=''
serverport=4304
srcphost = 'localhost'
srcpport = 4303

try:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print "Failed to create server socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
    sys.exit(-1);

print 'Server socket created'
 
try:
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((serverhost, serverport))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

try:
    srcpip=socket.gethostbyname(srcphost)
except:
    print "Hostname "+srcphost+" could not be resolved. Exiting"
    sys.exit(-3)
    
print "Ip adress of "+srcphost+" is "+srcpip

serversocket.listen(10)

print 'Socket now listening'

count = 0

while True:
    #wait to accept a connection - blocking call
    client, addr = serversocket.accept()    
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    try:
        srcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error, msg:
        print "Failed to create srcp socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
        sys.exit(-2);
    srcpsock.connect((srcpip , srcpport))
     
    print 'Socket Connected to ' + srcphost + ' on ip ' + srcpip
    
    welcome = srcpsock.recv(1024)
    print welcome
    client.send(welcome)    
       
    #infinite loop so that function do not terminate and thread do not end.
    while True:         
        #Receiving from client
        data = client.recv(1024)
        if not data:
            break;
        print data
        srcpsock.sendall(data)
        
        data = srcpsock.recv(1024)
        if not data:
            break;
        print data
        client.sendall(data)
        count+=1
        if count==10:
            print clock()
            data="1395801645.766 100 INFO 1 FB 64 1\n"
            print "interfering: "+data
            client.sendall(data)
            data="1395801645.766 100 INFO 2 FB 64 1\n"
            print "interfering: "+data
            client.sendall(data)
            data="1395801645.766 100 INFO 64 1\n"
            print "interfering: "+data
            client.sendall(data)
            data="100 INFO 64 1\n"
            print "interfering: "+data
            client.sendall(data)
        if count==11:
            data="1395801645.766 100 INFO 1 FB 64 0\n"
            print "interfering: "+data
            client.sendall(data)
            data="1395801645.766 100 INFO 2 FB 64 0\n"
            print "interfering: "+data
            client.sendall(data)
            data="1395801645.766 100 INFO 64 0\n"
            print "interfering: "+data
            client.sendall(data)
            data="100 INFO 64 0\n"
            print "interfering: "+data
            client.sendall(data)
            count=0
    #came out of loop
    srcpsock.close()
    client.close()
    print "connection closed"
 
serversocket.close()
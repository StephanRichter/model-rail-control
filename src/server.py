#!/usr/bin/python
# coding=utf8
import socket,sys,time;
from thread import *

#try:
#    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#except socket.error, msg:
#    print "Failed to create socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
#    sys.exit();
#
#print "socket created"
#
#host = 'localhost'
#port = 4303
#try:
#    remote_ip=socket.gethostbyname(host)
#except:
#    print "Hostname "+host+" could not be resolved. Exiting"
#    sys.exit()
#    
#print "Ip adress of "+host+" is "+remote_ip
#
#s.connect((remote_ip , port))
# 
#print 'Socket Connected to ' + host + ' on ip ' + remote_ip
#
#welcome = s.recv(1024)
#print welcome
#
#def send(msg):
#    print "Sending "+msg
#    try:
#        s.sendall(msg+"\n")
#    except socket.error:
#        print 'Send failed'
#        sys.exit()
#    reply = s.recv(1024)
#    print reply
#
#
#send("SET PROTOCOL SRCP 0.8.4")
#send("GO")
#send("INIT 1 GA 1 N")
#send("SET 1 POWER ON")
#time.sleep(1)
#send("SET 1 GA 1 0 1 100")
#time.sleep(1)
#send("SET 1 GA 1 1 1 100")
#time.sleep(1)
#s.close()

HOST=''
PORT=8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Socket created'
 
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data:
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
    print "connection closed"

while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
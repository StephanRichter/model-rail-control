#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
from MCP23S17 import *

class RocrailProxy(object):
    def __init__(self,host,port):
        print "Creating new SRCP proxy @ {}:{}".format(host,port)
        self.host=host
        self.port=port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def recv(self):
        return self.socket.recv(1024)
    
    def send(self,data):
        self.socket.sendall(data)
        
    def sensorThread(self,client):
        old=0
        time.sleep(1)
        while True:
            val=0
            for chip in (self.sensors):
                val<<=16
                val = val|chip.readSPI()

            diff=old^val

            for i in range(16*len(self.sensors),0,-1):
                if 1<<i-1 & diff:
                    if 1<<i-1 & val:
                        msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
                    else:
                        msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";
                    client.sendall(msg+"\n")
            old=val
            
            time.sleep(0.01)
          
    def connect(self,source,sink,connection):
        while True:
            data=source.recv(1024)
            if not data:
                break
            print "[{}] ".format(connection)+data.strip()
            #time.sleep(0.1)
            sink.sendall(data)
            if data=="SET CONNECTIONMODE SRCP INFO\n":
                start_new_thread(self.sensorThread, (source,))
        try:
            source.close()
        except:
            pass
            
    def process(self,client,connection,signalDriver):
        client.sendall("RocrailProxy V0.1; SRCP 0.8.4\n");
        while True:
            data=client.recv(1024)
            if not data:
                break
            data = data.strip()
            response = "410 ERROR unknown command";
            if 'SET PROTOCOL SRCP' in data:
                response = "201 OK PROTOCOL SRCP";                     
            if data == 'SET CONNECTIONMODE SRCP COMMAND':
                response = "202 OK CONNECTIONMODE"
            if data == 'SET CONNECTIONMODE SRCP INFO':
                response = "202 OK CONNECTIONMODE"
            if data == 'GO':
                response = "100 OK GO {}".format(connection)
            if data == 'GET 1 POWER':
                response = "100 INFO 1 POWER ON"
            if 'GET 1 GA' in data:
                response = "100 "+data.replace('GET','100 INFO')+" 1"
            if "SET 1 GA" in data:
                dummy=data.replace('SET 1 GA ','');
                parts = dummy.split(' ')
                addr=parts[0]
                state=parts[1]
                flag=parts[2]
                if signalDriver.handle(int(addr),int(state),int(flag)):
                    response = "200 OK"
                    
            response="{} ".format(time.time())+response;
            client.sendall(response+"\n")
        try:
            print "connection {} closed".format(connection)
            client.close()
        except:
            pass
        
    def forward(self,srcpSock):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host,self.port))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(-3) 
        
        
        self.srcp=srcpSock
        self.socket.listen(10)
        print 'Bound to server socket, listening.'
            
        connection=0
                     
        while True:
            client, addr = self.socket.accept()
            print 'Incoming connection from {}:{}...'.format(addr[0],addr[1]);
            self.srcp.connect();
            start_new_thread(self.connect, (client,self.srcp.socket,connection,))
            start_new_thread(self.connect, (self.srcp.socket,client,connection,))
            connection+=1    
 
        serversocket.close()

    def addSensors(self,sensors):
        self.sensors=sensors

    def connectTo(self,signalDriver):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host,self.port))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(-3) 
        
        
        self.socket.listen(10)
        print 'Bound to server socket, listening.'
            
        connection=0
                     
        while True:
            client, addr = self.socket.accept()
            print 'Incoming connection from {}:{}...'.format(addr[0],addr[1]);
            start_new_thread(self.process, (client,connection,signalDriver,))
            connection+=1    
 
        serversocket.close()
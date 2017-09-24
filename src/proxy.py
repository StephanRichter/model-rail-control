#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
from SensorChipFactory import *

class SRCPSock(object):

    def recv(self):
        return self.socket.recv(1024);
    
    def send(self,message):
        self.socket.sendall(message)

    def close(self):
        self.socket.close();
        print "Disconnected from SRCP!"
    
    def __init__(self,host,port):
        self.port=port
        try:
            self.host=socket.gethostbyname(host)
        except:
            print "Hostname "+host+" could not be resolved. Exiting"
            sys.exit(-2)            
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print "Client socket created."        
        except socket.error, msg:
            print "Failed to create socket. Error code: "+str(msg[0])+", Error message: "+msg[1]
            sys.exit(-1)
        self.socket.connect((self.host , self.port))
        print "SRCP connected @ {}:{}".format(self.port,self.host);
        
        
    def setup(self):
        self.connect();
        welcome = self.recv()
        print "Connected to SRCP:"
        print welcome
        self.send("SET PROTOCOL SRCP 0.8\n")
        self.send("SET CONNECTIONMODE SRCP COMMAND\n")
        self.send("GO\n")
        self.send("SET 1 POWER ON\n")
        for addr in range(1,40):
            time.sleep(0.01)
            self.send("INIT 1 GL "+str(addr)+" N 1 128 4\n")
            self.send("INIT 1 GA "+str(addr)+" N\n")
        self.send("TERM 0 SESSION\n")
        self.close()

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
        
    def sensorThread(self,source):
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
                    
                    #prnt(msg,True)
                    source.sendall(msg+"\n")
            old=val
            
            time.sleep(0.01)
        
    def client2srcp(self,source,connection):
        while True:
            data=source.recv(1024)
            if not data:
                break
            self.srcp.send(data)
            if data=="SET CONNECTIONMODE SRCP INFO\n":
                self.infoSession[connection]=True
                start_new_thread(self.sensorThread, (source,))
        try:
            source.close()
        except:
            pass
            
    def srcp2client(self,sink,connection):
        while True:
            data=self.srcp.recv()
            if not data:
                break
            sink.sendall(data)
        try:
            self.srcp.close()
        except:
            pass
        
    def connect(self,client,connection):    
        self.srcp.connect();
        start_new_thread(self.client2srcp, (client,connection,))
        start_new_thread(self.srcp2client, (client,connection,))
        
    def listen(self,srcpSock):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host,self.port))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(-3) 
        
        print 'Bound to server socket.'

        self.srcp=srcpSock
        self.socket.listen(10)
        print 'Listening.'
            
        connection=0
        self.infoSession=[]
                     
        while True:
            client, addr = self.socket.accept()
            self.infoSession.append(False)
            print 'Incoming connection from {}:{}...'.format(addr[0],addr[1]);
            self.connect(client,connection)
            connection+=1    
 
        serversocket.close()

    def addSensors(self,sensors):
        self.sensors=sensors
     
if __name__ == "__main__":

    sensorChipFactory = SensorChipFactory(12,16,18,22)
    #signalChipFactory = signalChipFactory(SIGNAL_CS,SIGNAL_SCLK,SIGNAL_MOSI,SIGNAL_MISO)
    
    sensors=(sensorChipFactory.provide(3),
        sensorChipFactory.provide(0),
        sensorChipFactory.provide(1),
        sensorChipFactory.provide(2))
    
    srcpSock = SRCPSock('localhost',4303);
    srcpSock.setup()
    
    proxy = RocrailProxy('localhost',4304);
    proxy.addSensors(sensors)
    proxy.listen(srcpSock)
#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread
import RPi.GPIO as GPIO

class SRCPProxy(object):

    def __init__(self,host,port):
        print "Creating new SRCP proxy @ {}:{}".format(host,port)
        self.host=host
        self.port=port
        self.errorPin = 0
        self.errorFeedback = 0
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    def recv(self):
        return self.socket.recv(1024)
    
    def send(self,data):
        self.socket.sendall(data)
        
    def sensorThread(self,client):
        old=0
        time.sleep(1)
        error = 0
        while True:
            val = self.sensors.readValue()
            
            diff=old^val

            for i in range(self.sensors.contacts,0,-1):
                if 1<<i-1 & diff:
                    if 1<<i-1 & val:
                        msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
                    else:
                        msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";
                    client.sendall(msg+"\n")
                    print msg
            old=val

            
            if bool(GPIO.input(self.errorPin)) != self.errorPullup:
                if not error:
                    msg=str(time.time())+" 100 INFO 0 FB "+str(self.errorFeedback)+" 1";
                    client.sendall(msg+"\n")
                    print "Error detected! -- "+msg
                    error = 1
            else:
                if error:
                    msg=str(time.time())+" 100 INFO 0 FB "+str(self.errorFeedback)+" 0";
                    client.sendall(msg+"\n")
                    error = 0
            
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
        client.sendall("SRCP Proxy V0.2; SRCP 0.8.4\n");
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

    def setErrorInput(self,errorPin,pullUp,errorFeedback):
        self.errorPullup = pullUp
        self.errorFeedback = errorFeedback
        self.errorPin = errorPin
        if pullUp:
            GPIO.setup(errorPin,GPIO.IN,pull_up_down=GPIO.PUD_UP);
        else:
            GPIO.setup(errorPin,GPIO.IN);
        print "set up error detection on pin ",self.errorPin
    

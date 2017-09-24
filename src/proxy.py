#!/usr/bin/python
import socket,sys, time
from thread import start_new_thread

class SRCPSock(object):

    def recv(self):
        return self.socket.recv(1024);
    
    def send(self,message):
        self.socket.sendall(message+"\n")
        reply=self.recv()

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
        self.send("SET PROTOCOL SRCP 0.8")
        self.send("SET CONNECTIONMODE SRCP COMMAND")
        self.send("GO")
        self.send("SET 1 POWER ON")
        for addr in range(1,40):
            time.sleep(0.01)
            self.send("INIT 1 GL "+str(addr)+" N 1 128 4")
            self.send("INIT 1 GA "+str(addr)+" N")
        self.send("TERM 0 SESSION")
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
        
    def client2srcp(self,socket,connection):
        while True:
            data=socket.recv(1024)
            if not data:
                break
            print "client == {} ==> srcp".format(data.strip());
            self.srcp.send(data)
            if data=="SET CONNECTIONMODE SRCP INFO\n":
                self.infosession[connection]=True
                start_new_thread(sensorThread)
        try:
            print "Closing client socket!"
            socket.close()
            
        except:
            pass
        
    def srcp2client(self,socket,connection):
        while True:
            data=self.srcp.recv()
            if not data:
                break
            print "client <== {} == srcp".format(data.strip());
            socket.sendall(data)
        try:
            self.srcp.close()
        except:
            pass
        
    def connect(self,client,connection):    
        self.srcp.connect();
        start_new_thread(self.srcp2client, (client,connection,))
        start_new_thread(self.client2srcp, (client,connection,))
        
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

     
if __name__ == "__main__":
    srcpSock = SRCPSock('localhost',4303);
    srcpSock.setup()
    
    proxy = RocrailProxy('localhost',4304);
    proxy.listen(srcpSock)

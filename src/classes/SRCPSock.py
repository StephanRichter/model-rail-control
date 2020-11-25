#!/usr/bin/python
import socket,sys, time

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
        
    def setup(self,loco_count,acc_count):
        self.connect();
        welcome = self.recv()
        print "Connected to SRCP:"
        print welcome
        self.send("SET PROTOCOL SRCP 0.8\n")
        self.send("SET CONNECTIONMODE SRCP COMMAND\n")
        self.send("GO\n")
        self.send("SET 1 POWER ON\n")
        for addr in range(1,loco_count+1):
            time.sleep(0.01)
            self.send("INIT 1 GL "+str(addr)+" N 1 128 4\n")
            
        for addr in range(1,acc_count):
            time.sleep(0.01)
            self.send("INIT 1 GA "+str(addr)+" N\n")
        self.send("TERM 0 SESSION\n")
        self.close()

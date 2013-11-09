r"""
srcp.py
Version 0.9.2
# (c) Matthias Trute 2004,2005; published under the  GNU License V2, 1991

"""

import string, socket

# defaults

host = "localhost"
port = 4303
srcp = "0.8.4"


#
def DBG(s): return 1
#def DBG(s): print s; return 1
#def DBG(s,f=open('/dev/tty4','w')): f.write(s + '\n'); f.flush(); return 1
#def DBG(s,f=open('/dev/pts/4','w')): f.write(s + '\n'); f.flush(); return 1
#def DBG(s,f=open('srcpy.log','w')): f.write(s + '\n'); f.flush()

class Error(Exception):
    pass

class SRCP_Error(Error):
    def __init__(self, codelist, command):
        Error.__init__(self, codelist)
        self.timestamp = codelist[0]
        self.errorcode = int(codelist[1])
        self.msg = codelist[3:]
        self.command = command
    def __str__(self):
        return "%s ERROR %s %s: %s" % (self.timestamp, self.errorcode, self.msg, self.command)

class srcp_connection:
    """
    Handle the connection to the SRCP server.
    """
    __srcpversion = None
    __sessionid = 0
    __IGNORE_412_416 = 0
    def __init__(self):
        self.__s = None
        self.__connected = 0
        self.host = None
        self.port = None

    def handshake(self):
        raise Error, "Sorry, no connection mode specified: please consult SRCP, if you want a command session, use the commandsession class."

    def checkWelcome(self, welcome):
        for s in string.split(welcome, ";"):
            (k, v) = string.split(s, " ", 1);
            if k ==  "SRCP":
                self.__srcpversion = v

    def requireSRCP(self, version):
        self.command("SET PROTOCOL SRCP %s" % version)

    def connect(self, host='localhost', port=12345):
        """Establish the connection to the SRCP server

        host and port specifiy the parameters of how to connect the server.
        If the connection could not be established the according exception
        will be raised.

        """
        if self.__connected: raise Error, 'already connected'
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connected = 1
        self.host = host
        self.port = port
        try:
            self.__s.connect( (host, port) )
            self.__f = self.__s.makefile('r')
            self.__welcome = self.readline()
            self.checkWelcome(self.__welcome)
            self.requireSRCP(srcp)
            self.handshake()
            s = string.split(self.command("GO"))
            self.__sessionid = int(s[4])
            return
        except socket.error:
            self.__s.close()
            self.__s = None
            raise

    def connected(self):
        # Connection to server established?
        return self.__s != None

    def sessionid(self):
        return self.__sessionid

    def sendline(self, s):
        """
        Send a command to the SRCP server.
        """
        DBG('sent [%s]: %s' % (self.sessionid(), s))
        # add terminating '\n';
        if s[-1] <> '\n':
            s = s + '\n'
        if not self.__connected:
            raise Error, 'not connected'
        if not self.__s: return
        self.__s.send(s)

    def readline(self):
        line = self.__f.readline()
        while line[-2]=='\\':
            line = line[:-2]
            line = line + self.__f.readline()
        DBG('recv [%s]: %s' % (self.sessionid(), line[:-1]))
        return line

    def command(self, cmd):
        self.sendline(cmd)
        r = self.readline()
        w = string.split(r)
        if int(w[1])>399:
            if ( self.__IGNORE_412_416 == 1) and (int(w[1])==412 or int(w[1])==416):
                return r
            else:
                raise SRCP_Error(w, cmd)
        return r

    def setignore_412_416(self, v):
        DBG( "setignore (%s)" % v )
        self.__IGNORE_412_416 = v


######################################
# infosession starts an info session (sic!). It
# contains a thread function to keep all
# objects up to date.
class infosession(srcp_connection):
    def __init__(self, host=host, port=port):
        srcp_connection.__init__(self)
        self.__srcpobjs = []
        self.connect(host, port)
    def handshake(self):
        self.command("SET CONNECTIONMODE SRCP INFO")

    def addListener(self, srcpobj):
        self.__srcpobjs.append(srcpobj)

    def delListener(self, srcpobj):
        self.__srcpobjs.remove(srcpobj)

    def update(self, line):
        w = string.split(line)
        for srcpobj in self.__srcpobjs:
            if srcpobj.match(w):
                srcpobj.updatefromserver(w)

    def mainloop(self):
        while(1):
            line = self.readline()
            self.update(line)

    def monitor(self):
        import threading
        t = threading.Thread(target=self.mainloop)
        t.setDaemon(1)
        t.start()

############################################
#
class commandsession(srcp_connection):
    def __init__(self, host=host, port=port):
        srcp_connection.__init__(self)
        self.connect(host, port)

    def handshake(self):
        self.command("SET CONNECTIONMODE SRCP COMMAND")

    def __call__(self, command):
        return self.command(command)

######################################################################
#
# two session objects. Will be initialized when this module is used
# as a library. see the end of this file.

srcpinfo=None
srcpcommand=None

#################################################
# base object
#################################################
class srcp_object:
    def __init__(self, bus, devicegroup):
        self.bus = int(bus)
        self.devicegroup = devicegroup
        self.__callbacks = []
        srcpinfo.addListener(self)

    def __str__(self):
        r = "SRCP Object %d %s" % (self.bus, self.devicegroup)
        return r

    def destroy(self):
        self.__callbacks = []
        srcpinfo.delListener(self)

    def addCallback(self, proc):
        self.__callbacks.append(proc)

    def updatefromserver(self, info):
        for proc in self.__callbacks:
            proc(info)

    def match(self, info):
        return 0

##################################
#
class BUS(srcp_object):
    state = "unknown"

    def __init__(self, id):
        self.busnumber = id
        srcp_object.__init__(self, id, "POWER")
        self.getPower()

    def powerOff(self):
        srcpcommand.command("SET %d POWER OFF" % self.busnumber)

    def powerOn(self):
        srcpcommand.command("SET %d POWER ON" % self.busnumber)

    def getPower(self):
        r = srcpcommand.command("GET %d POWER" % self.busnumber)
        DBG( "getPower r=%s" % r )
        w = string.split(r)
        if self.match(w):
            DBG('Value received : %s' % r)
            self.updatefromserver(w)
        else:
          DBG('Unexpected value received : %s' % r)
          print 'Unexpected value received : %s' % r
          if int(w[1]) >= 400:
            self.state = "unknown"

    def getstate(self):
        return self.state

    def updatefromserver(self, info):
        self.state = info[5]
        return 0

    def match(self, info):
        DBG( "match(self %s, info %s)" % (self, info))
        if int(info[1])==100 and int(info[3])==self.bus and info[4]=='POWER':
            return 1
        return 0

###################################
#
class SM(srcp_object):
    """
    General class to handle service mode devices
    """
    state = 0

    def __init__(self, bus, addr, smtype):
        srcp_object.__init__(self, bus, "SM")
        self.addr   = int(addr)
        self.smtype = smtype

    def __str__(self):
        r = 'SRCP SM %d %d: %d' % (self.bus, self.addr,self.smtype)
        return r

    def match(self, info):
        if int(info[1])==100 and int(info[3])==self.bus and info[4]=='SM' and int(info[5])==self.addr:
            return 1
        return 0

    def updatefromserver(self, info):
        self.state = int(info[6])
        srcp_object.updatefromserver(self, info)

class CV(SM):
        def __init__(self, bus, addr):
            SM.__init__(self, bus, addr)
        def GET(self, cv):
            srcpcommand.command("GET %d SM %d CV %d" % (self.bus, self.addr, cv))


###################################
#
class FB(srcp_object):
    """
    General class to handle feedback devices
    """
    state = 0

    def __init__(self, bus, addr):
        DBG('Initializing Bus %s FB %s' % (bus, addr))
        srcp_object.__init__(self, bus, "FB")
        self.addr   = int(addr)
        # after init get current state (it might already be 1)
        DBG('Asking for FB state Bus %s addr %s' % (self.bus, self.addr))
        r = srcpcommand.command('GET %s FB %s' % (self.bus, self.addr))
        # print "r=", r
        w = string.split(r)
        if self.match(w):
            DBG('Value received : %s' % r)
            self.updatefromserver(w)
        else:
          DBG('Unexpected value received : %s' % r)
          print 'Unexpected value received : %s' % r
          if int(w[1]) >= 400:
            self.state=-1

    def __str__(self):
        r = 'SRCP Feedback %d %d: %d' % (self.bus, self.addr,self.state)
        return r

    def match(self, info):
        if int(info[1])==100 and int(info[3])==self.bus and info[4]=='FB' and int(info[5])==self.addr:
            return 1
        return 0

    def updatefromserver(self, info):
        self.state = int(info[6])
        srcp_object.updatefromserver(self, info)

    def wait(self, state, delay=1000, server=srcpcommand):
        command = 'WAIT %s FB %s %s %s' % (self.bus, self.addr, state, delay)
        return server.command(command)

    def getstate(self):
        return self.state


###############################
#
class TIME(srcp_object):
    """
    General class to handle time
    """

    def __init__(self):
        srcp_object.__init__(self, 0, "TIME")

    def match(self, info):
        if int(info[1])==100 and int(info[3])==0 and info[4]=='TIME':
            return 1
        return 0

    def updateDay(self, d):
        self.d = int(d)

    def updateHour(self, h):
        self.h = int(h)

    def updateMinute(self, m):
        self.m = int(m)

    def updateSecond(self, s):
        self.s = int(s)

    def updatefromserver(self, info):
        self.updateDay(info[5])
        self.updateHour(info[6])
        self.updateMinute(info[7])
        self.updateSecond(info[8])
        srcp_object.updatefromserver(self, info)

    def init(self, d, h, m, s, fx=None, fy=None):
        if not (fx==None or fy==None):
            srcpcommand.command("INIT 0 TIME %d %d" % (fx, fy))
        srcpcommand.command("SET 0 TIME %d %d %d %d" % (d, h, m, s))


###########################################
#
class GL(srcp_object):
    """
    General class to handle GL devices
    autosend: whenever a setxx method is called, the send() method is invoked
    """
    f = []
    maxspeed = 0
    lock = 0

    def __init__(self, bus, addr, autosend=0):
        srcp_object.__init__(self, bus, "GL")
        self.addr   = int(addr)
        self.autosend = autosend
        try:
            self.description = string.split(srcpcommand.command("GET %d DESCRIPTION GL %d" % (bus, addr)))
            self.srcpupdate()
        except:
            self.description = None

    def __str__(self):
        r = 'GL %d-%d (%s)' % (self.bus, self.addr, id(self) )
        return r

    def match(self, info):
        if int(info[1])==100 and int(info[3])==self.bus and info[4]=='GL' and int(info[5])==self.addr:
            return 1
        return 0

    def lock(self, duration=100, server=srcpcommand):
        cmd = "SET %d LOCK GL %d %d" % (self.bus, self.addr, duration)
        try:
            server.command(cmd)
        except:
            pass

    def unlock(self, server=srcpcommand):
        cmd = "TERM %d LOCK GL %d" % (self.bus, self.addr)
        try:
            server.command(cmd)
        except:
            pass

    def init(self, protocol, protocolversion, nfs, nf):
        ''' init a new loco
            after init the description must be updated because it is None
        '''
        srcpcommand.command("INIT %d GL %d %s %s %d %d" % (self.bus, self.addr, protocol, protocolversion, nfs, nf))
        self.description = string.split(srcpcommand.command("GET %d DESCRIPTION GL %d" % (self.bus, self.addr)))

    def term(self):
        srcpcommand.command("TERM %d GL %d " % (self.bus, self.addr))

    def reset(self):
        srcpcommand.command("RESET %d GL %d " % (self.bus, self.addr))


    def srcpupdate(self, server=srcpcommand):
        cmd = "GET %d GL %d" % (self.bus, self.addr)
        DBG(cmd)
        if not server:
            server = srcpcommand
        r = server(cmd)
        DBG(r)
        w = string.split(r)
        self.updatefromserver(w)

    def updateDirection(self, value):
        self.direction = value

    def updateSpeed(self, value):
        self.speed = value

    def updateDecoderspeed(self, value):
        self.decoderspeed = value
        if self.maxspeed==0:
            self.maxspeed=self.decoderspeed

    def updateFunctions(self, value):
        self.f = value

    def updatefromserver(self, info):
        self.updateDirection(int(info[6]))
        self.updateSpeed(int(info[7]))
        self.updateDecoderspeed(int(info[8]))
        self.updateFunctions(info[9:])
        srcp_object.updatefromserver(self, info)

    def getSpeed(self):
        return self.speed

    def getMaxspeed(self):
        return self.maxspeed

    def getF(self, i):
        return self.f[i]

    def getDirection(self):
        return self.direction

    def setSpeed(self,speed):
        self.speed=speed
        if self.autosend==1:
            self.send()

    def notstop(self):
        self.setDirection(2)
        self.send()

    def setMaxspeed(self, maxspeed):
        self.maxspeed=maxspeed
        if self.autosend==1:
            self.send()

    def setF(self, i, f):
        self.f[i]=f
        if self.autosend==1:
            self.send()

    def setDirection(self, direction):
        self.direction=direction
        if self.autosend==1:
            self.send()

    def send(self, server=srcpcommand):
        if not server:
            server = srcpcommand
        server.command(self.srcp())

    def srcp(self):
        r = 'SET %d GL %d %d %d %d' % (self.bus, self.addr, self.direction, self.speed, self.maxspeed)
        for f in self.f:
            r = '%s %s' % (r, f)
        return r
#############################################
#
class GA(srcp_object):
    """
    General class to handle GA devices
    """
    lastporttime = 0
    lastport = 0
    state = [0,0]

    def __init__(self, bus, addr):
        srcp_object.__init__(self, bus, "GA")
        self.addr   = int(addr)
        try:
            self.description = srcpcommand.command("GET %d DESCRIPTION GA %d" % (bus, addr))
        except:
            pass
        # all GA have two ports.. ;=)
        self.state = [0,0]
        self.srcpupdate()

    def init(self, protocol):
        ''' init a new accessory
            after init the description must be updated because it is None
        '''
        srcpcommand.command("INIT %d GA %d %s " % (self.bus, self.addr, protocol))
        self.description = srcpcommand.command("GET %d DESCRIPTION GA %d" % (self.bus, self.addr))

    def term(self):
        srcpcommand.command("TERM %d GA %d " % (self.bus, self.addr))

    def reset(self):
        srcpcommand.command("RESET %d GA %d " % (self.bus, self.addr))


    def srcpupdate(self, server=srcpcommand):
        if not server:
            server = srcpcommand
        for port in range(0, len(self.state)):
            try:
                r = server.command("GET %d GA %d %d" % (self.bus, self.addr, port))
                w = string.split(r)
                self.updatefromserver(w)
            except:
                pass

    def __str__(self):
        r = 'GA: %d %d' % (self.bus, self.addr)
        return r

    def match(self, info):
        if int(info[1])==100 and int(info[3])==self.bus and info[4]=='GA' and int(info[5])==self.addr:
            return 1
        return 0

    def updatefromserver(self, info):
        self.state[int(info[6])] = int(info[7])
        # lastport aktualisieren
        time = string.atof(info[0])
        if self.lastporttime < time:
            self.lastporttime = time
            self.lastport = int(info[6])
        srcp_object.updatefromserver(self, info)

    def lock(self, duration=100, server=srcpcommand):
        if not server:
            server = srcpcommand
        cmd = "SET %d LOCK GA %d %d" % (self.bus, self.addr, duration)
        try:
            server.command(cmd)
        except:
            pass

    def unlock(self):
        cmd = "TERM %d LOCK GA %d" % (self.bus, self.addr)
        try:
            srcpcommand(cmd)
        except:
            pass


    def actuate(self, port, state, delay=100):
        command = 'SET %d GA %d %d %d %d' % (self.bus, self.addr, port, state, delay)
        srcpcommand(command)

    def toggle(self):
        """toggles the current state of the accessory"""
        self.actuate(not self.lastport, 1)

##################################
# initialization.
# format of the srcpd_rc is identical to
# the tcl lib.

try:
    import os
    import re
    f = open(os.environ.get("HOME") + "/.srcp_rc", "r")
    for line in f.readlines():
        w = string.split(line, "=")
        if len(w) > 1:
            if re.match("srcpserver", w[0]):
                host = w[1].strip("\n ")
            if re.match("srcpport", w[0]):
                port = int(w[1].strip("\n "))
except Exception, e:
    pass

srcpinfo = infosession(host, port)
srcpcommand = commandsession(host, port)
TIME = TIME()

if __name__ == '__main__':
    srcpinfo.mainloop()
else:
    srcpinfo.monitor()

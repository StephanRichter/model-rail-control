# coding=utf8
import time,srcp

entkuppler3=srcp.GA(1,7)
entkuppler3.init("N")
entkuppler2=srcp.GA(1,6)
entkuppler2.init("N")
weiche12=srcp.GA(1,5)
weiche12.init("N")
weiche1=srcp.GA(1,1)
weiche1.init("N")
weiche2=srcp.GA(1,2)
weiche2.init("N")
weiche3=srcp.GA(1,3)
weiche3.init("N")
weiche34=srcp.GA(1,8)
weiche34.init("N")
weiche4=srcp.GA(1,4)
weiche4.init("N")
weiche5=srcp.GA(1,5)
weiche5.init("N")
weiche9=srcp.GA(1,9)
weiche9.init("N")
weiche10=srcp.GA(1,10)
weiche10.init("N")

def ausfahrt1():
    print "Weichenstraße Ausfahrt 1"
    weiche4.actuate(0, 1)
    time.sleep(1)
    weiche2.actuate(0, 1)      

def ausfahrt2():
    print "Weichenstraße Ausfahrt 2"
    weiche4.actuate(1, 1)
    time.sleep(1)
    weiche2.actuate(0, 1)

def ausfahrt3():
    print "Weichenstraße Ausfahrt 3"
    weiche2.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche3.actuate(0, 1)
    time.sleep(1)
    weiche34.actuate(0, 1)
      
def ausfahrt4():
    print "Weichenstraße Ausfahrt 4"
    weiche2.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche3.actuate(1, 1)
    time.sleep(1)
    weiche34.actuate(0, 1)

def einfahrt1():
    print "Weichenstraße Einfahrt 1"
    weiche4.actuate(0, 1)
    time.sleep(0.5)
    weiche1.actuate(1, 1)
    time.sleep(0.5)
    weiche5.actuate(0, 1)            

def einfahrt2():
    print "Weichenstraße Einfahrt 2"
    weiche4.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(1, 1)
    time.sleep(1)
    weiche4.actuate(1, 1)            
    time.sleep(1)
    weiche5.actuate(0, 1)            

def einfahrt3():
    print "Weichenstraße Einfahrt 3"
    weiche3.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)            
    time.sleep(1)
    weiche34.actuate(0, 1)

def einfahrt4():
    print "Weichenstraße Einfahrt 4"
    weiche3.actuate(1, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)            
    time.sleep(1)
    weiche34.actuate(0, 1)

def entkupplenLinks(count=1):
    for i in range(count,0,-1):
        weiche9.actuate(0, 1,1000)
        time.sleep(0.2*i)

def entkuppeln3():
    entkuppler3.actuate(0, 1)
    time.sleep(0.2)
        
def bahnhofLinksAbzweig():
    print "Weichenstraße Bahnhof (links) Abzweig"
    weiche10.actuate(0, 1)
    time.sleep(1)
    weiche10.actuate(0, 1)

def bahnhofLinksGerade():
    print "Weichenstraße Bahnhof (links) Gerade"
    time.sleep(1)
    weiche9.actuate(1, 1)
    time.sleep(1)
    weiche9.actuate(1, 1)
    time.sleep(1)
    weiche9.actuate(1, 1)
    time.sleep(1)
    weiche10.actuate(1, 1)
    time.sleep(1)


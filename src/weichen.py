import time,srcp

entkuppler3=srcp.GA(1,7)
weiche1=srcp.GA(1,1)
weiche2=srcp.GA(1,2)
weiche3=srcp.GA(1,3)
weiche34=srcp.GA(1,8)
weiche4=srcp.GA(1,4)
weiche9=srcp.GA(1,9)
weiche10=srcp.GA(1,10)

def ausfahrt3():
    weiche2.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche3.actuate(0, 1)
      
def einfahrt3():
    weiche3.actuate(0, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)            

def einfahrt4():
    weiche3.actuate(1, 1)
    time.sleep(1)
    weiche1.actuate(0, 1)
    time.sleep(1)
    weiche4.actuate(0, 1)            

def entkupplenLinks(count=1):
    for i in range(count,0,-1):
        weiche9.actuate(0, 1,1000)
        time.sleep(0.2*i)
        
def bahnhofLinksGerade():
    time.sleep(2)
    weiche9.actuate(1, 1)
    time.sleep(1)
    weiche9.actuate(1, 1)
    time.sleep(1)
    weiche9.actuate(1, 1)
    time.sleep(2)
    weiche10.actuate(1, 1)
    time.sleep(2)


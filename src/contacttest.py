from SensorChipFactory import *

sensorChipFactory = SensorChipFactory(12,16,18,22)
#signalChipFactory = signalChipFactory(SIGNAL_CS,SIGNAL_SCLK,SIGNAL_MOSI,SIGNAL_MISO)

sensorChip3 = sensorChipFactory.provide(3);
sensorChip0 = sensorChipFactory.provide(0);
sensorChip1 = sensorChipFactory.provide(1);
sensorChip2 = sensorChipFactory.provide(2);

chips=(sensorChip3, sensorChip0, sensorChip1, sensorChip2)
old=0
while True:
    val=0
    for chip in (chips):
        val<<=16
        val = val|chip.readSPI()
        
        
    diff=old^val

    for i in range(16*len(chips),0,-1):
        if 1<<i-1 & diff:
            if 1<<i-1 & val:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 1";
            else:
                msg=str(time.time())+" 100 INFO 0 FB "+str(i)+" 0";
            
            print msg
    old=val
    
    time.sleep(0.01)
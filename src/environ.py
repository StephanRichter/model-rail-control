# coding=utf8
import myconsts
from platf import *
from station import *
from switches import *

l1=Platform("Gleis 1",124)
l2=Platform("Gleis 2",124)
l1.setDriveIn(bahnhofLinksGerade)
l2.setDriveIn(bahnhofLinksAbzweig)
l1.setBypass(l1,124,NACH_RECHTS)

r1=Platform("Gleis 1",130)
r2=Platform("Gleis 2",130)
r3=Platform("Gleis 3",120)
r4=Platform("Gleis 4",120)
r1.setDriveIn(einfahrt1)
r1.setDriveOut(ausfahrt1)
r2.setDriveIn(einfahrt2)
r2.setDriveOut(ausfahrt2)
r3.setDriveIn(einfahrt3)
r3.setDriveOut(ausfahrt3)
r4.setDriveIn(einfahrt4)
r4.setDriveOut(ausfahrt4)

r2.setBypass(r1,97,NACH_LINKS)
r3.setBypass(r4,87,NACH_LINKS)

l1.addTarget(r1)
l1.addTarget(r2)
l1.addTarget(r3)
l1.addTarget(r4)
l2.addTarget(r1)
l2.addTarget(r2)
l2.addTarget(r3)
l2.addTarget(r4)
r1.addTarget(l1)
r1.addTarget(l2)
r2.addTarget(l1)
r2.addTarget(l2)
r3.addTarget(l1)
r3.addTarget(l2)
r4.addTarget(l1)
r4.addTarget(l2)

bahnhofLinks=Station("Bahnhof Links")
bahnhofRechts=Station("Bahnhof Rechts")

bahnhofLinks.addPlatform(l1)
bahnhofLinks.addPlatform(l2)
bahnhofLinks.addContact(KONTAKT_EINFAHRT_LINKS)
bahnhofLinks.addContact(KONTAKT_ENTKUPPLER_LINKS)
bahnhofRechts.addPlatform(r1)
bahnhofRechts.addPlatform(r2)
bahnhofRechts.addPlatform(r3)
bahnhofRechts.addPlatform(r4)
bahnhofRechts.addContact(KONTAKT_EINFAHRT_RECHTS)
bahnhofRechts.addContact(KONTAKT_ENTKUPPLER_RECHTS2)
bahnhofRechts.addContact(KONTAKT_ENTKUPPLER_RECHTS3)

print "Environment imported."
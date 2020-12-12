model-rail-control
==================

== english version below ==

Python-Proxy zur Steuerung von Modellbahnanlagen

Bei diesem Python-Programm handelt es sich um einen Rückmelde-Decoder-Anschluss-Proxy.
Das ganze ist gedacht für Modellbahnanlagen die mit RocRail oder Web4Rail gesteuert werden und als Software-Zentrale den SRCP-Daemon verwenden.
Dieser Proxy schaltet sich zwischen diese beiden Programme und füttert RocRail mit Sensordaten eines S88-Rückmeldesystems.
Der Code ist geschrieben und getestet für den Raspberry Pi mit Debian Buster.

Ältere Versionen (Commit 02378c6dae0de1ac1062836d46221d2b2a14267f und älter) waren dagegen eigenständge Automatik-Steuerungen und nicht für den Betrieb mit RocRail oder Web4Rail vorgesehen.
Falls Sie eine eigene Modellbahnsteuerung bauen wollen Sollten Sie diese auf dem genannten Commit aufbauen.

== english ==

Python code controlling my model rail

This python project is a tiny feedback sensor integration proxy.
It is suited for model railroad layouts, that are controlled with RocRail or Web4Rail and use the SRCP daemon as software control center.
This proxy is interposed between those two software packages and provides feedback sensor data from an S88 bus system to the SRCP daemon. 
The code has been implemented for and tested with a Raspberry Pi running Debian Buster.

Older versions (Commit 02378c6dae0de1ac1062836d46221d2b2a14267f and before) were standalone control centers for railroad automation and are not suited for use with RocRail or Web4Rail.
If you want to build your own automation code, you should base it on the mentioned commit.

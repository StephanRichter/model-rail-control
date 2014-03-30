model-rail-control
==================

== english version below ==

Python-Proxy zur Steuerung von Modellbahnanlagen

Bei diesem Python-Programm handelt es sich um einen Rückmelde-Decoder-Anschluss-Proxy.
Das ganze ist gedacht für Modellbahnanlagen die mit RocRail gesteuert werden und als Software-Zentrale den SRCP-Daemon verwenden.
Dieser Proxy schaltet sich zwischen diese beiden Programme und füttert RocRail mit Sensordaten eines MCP23S17.
Der Code ist geschrieben und getestet für den Raspberry Pi mit Debian Wheezy.

Ältere Versionen (Commit 02378c6dae0de1ac1062836d46221d2b2a14267f und älter) waren dagegen eigenständge Automatik-Steuerungen und nicht für den Betrieb mit RocRail vorgesehen.
Falls Sie eine eigene Modellbahnsteuerung bauen wollen Sollten Sie diese auf dem genannten Commit aufbauen.

== english ==

Python code controlling my model rail

This python project is a tiny feedback sensor integration proxy.
It is suited for model railroad layouts, that are controlled with rocrail and use the SRCP daemon as software control center.
This proxy is interposed between those two software packages and provides feedback sensor data for a MCP23S17 port expander to RocRail. 
The code has been implemented for and tested with a Raspberry Pi running Debian Wheezy.

Older versions (Commit 02378c6dae0de1ac1062836d46221d2b2a14267f and before) were standalone control centers for railroad automation and are not suited for use with RocRail.
If you want to build your own automation code, you should base it on the mentioned commit.




The code contained in mcp23s17.py was provided by Erik Bartmann (http://erik-bartmann.de/), who kindly allowed me to re-use and propagate it:

Hallo Herr Richter,

nur zu!

Es freut mich, wenn ich etwas zu Ihrem Projekt beitragen konnte.

Viele Grüße

Erik Bartmann

Am 28.03.2014 09:22, schrieb Stephan Richter:
> Dieses ist eine E-Mail-Anfrage via http://erik-bartmann.de/ von:
> Stephan Richter <--------@---------.de>
>
> Hallo!
>
> Zunächst ein großes Lob für die Ein-/Ausführungen zur Verwendung der MCP23S17 mit dem Raspberry-Pi. Ich nutze das ganze um meine Modellbahn zu steuern, bzw. um Rückmeldungen von meiner Modellbahn am Computer zu erfassen.
>
> In diesem Context habe ich einen kleien python-Proxy geschrieben, der die erfassten Rückmeldedaten für die automatische Steuerung der Modellbahn in die Kommunikation zwischen ROCRAIL [1] und SRCPD [2] einschleift. Dieser verwendet ihren Code [3].
>
> Um das ganze als OpenSource zu gestalten möchte ich meinen Python-Code inklusive ihres Codes auf Github veröffentlichen, um meinen Teil zur Community beizutragen.
>
> Deshalb die Frage: Darf ich ihren Code (inklusive Angabe Ihrer Autorendaten) zusammen mit meinem Code auf Github online stellen?
>
> besten Dank schon mal!
>
>
> mit freundlichen Grüßen,
> Stephan Richter
>
> [1] http://rocrail.net
> [2] http://srcpd.sourceforge.net
> [3] http://erik-bartmann.de/programmierung/downloads2.html#RasPi > "Python-Skript zur Steuerung des MCP23S17 am Raspberry Pi (Teil 2)"
>
>


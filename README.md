# XSYS-rat
Any potentially malicious content in this repository is for testing/educational purposes and should be approached with caution.


XSYS-rat : (r)emote (a)ccess (t)rojan
     
   
This is a Remote Trojan program.
this program devided by 2 Modules:

    * RAT.py              - CLIENT
    * MissionControl.py   - MultiThread SERVER

RAT.py
- will sit on the target computer and try to maintain connection with the Server, while using a costomized socket using TCP connection protocol, to ensure all data delivary.
- support upload and download funcitions to proveide the Server with phisical data.
- return full access to the machine Shell remotly.


MissionControl.py
- runs on the attackers machine, postentialy enable to gain root access to each remote host connection. 
- maintain parallel connection for each client socket and support up to 128 connections stable and running.
- contain a terminal application base look on cli with custome display.


Have a look :)

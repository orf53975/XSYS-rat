# XSYS-rat
Any potentially malicious content in this repository is for testing/educational purposes and should be approached with caution.


XSYS-rat : (R)emote (A)ccess (T)rojan
     
   
This is a Remote Trojan program.
this program devided by 3 Modules:

    # Client:
    * RAT.py              - Client App
    * RAW.py              - Crypto Module (File Cryptography)
    
    # Server:
    * MissionControl.py   - MultiThreaded Server App
    * FreeDNS.py          - Dynamic DNS Updater
    * Cronosphere.sh      - Shell Script Cron Job  

----------------------------------------------------------------
RAT.py
- will sit on the target computer and try to maintain connection with the Server, while using a costomized socket using TCP connection protocol, to ensure all data delivary.
- support upload and download funcitions to proveide the Server with phisical data.
- return full access to the machine Shell remotly.
----------------------------------------------------------------
RAW.py
- handled by RAT.py, this module handle all files encryption and decryption.
- using the capabilities given by pycrypto libs to control the encryption and hashing algorithms,
generally using AES.MODE_CBC as cipher and SHA256 to Hash a given KeyPhrase
----------------------------------------------------------------
MissionControl.py
- runs on the attackers machine, postentialy enable to gain root access to each remote host connection. 
- maintain parallel connection for each client socket and support up to 128 connections stable and running.
- contain a terminal application base look on cli with custome display.
----------------------------------------------------------------
FreeDNS.py
- this module resposible to update 
----------------------------------------------------------------
Cronosphere.sh
- a cron alike job maker, using Bash Script that execute FreeDNS.py every 300 seconds (5minutes) once you launch it
----------------------------------------------------------------

Have a look :)

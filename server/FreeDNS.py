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
	import urllib2
	import pip	
except ImportError as e:
	pip = lambda : os.system('pip install ' + str(e)[15:])
	pip()


class Updater:

	FreeDNS_URL = 'http://freedns.afraid.org/dynamic/update.php?'
	IP_SOURCER = 'http://ip.dnsexit.com/'
	OLDIP_FILE = os.getcwd() + '/ip.old'
	USER_KEYS = ["ejUyTlZFd1NVMXVMU2RGZDEzS2d0YUd3OjE3MjI5NDIx"]


	def __init__(self):
		self.start()


	def start(cls):
		new_ip = cls.url_stripper(cls.IP_SOURCER)
		if(not os.path.exists(cls.OLDIP_FILE)):
			cls.update_dns(new_ip)
		else:
			f = open(cls.OLDIP_FILE, 'r')
			old_ip = f.read()
			f.close()
			if(old_ip != new_ip):
				cls.update_dns(new_ip)


	def update_dns(cls, ip):
		for key in cls.USER_KEYS:
			print "{}".format(str(cls.url_stripper(cls.FreeDNS_URL + key)))
		f = open(cls.OLDIP_FILE, 'w+')
		f.write(ip)
		f.close()


	def url_stripper(cls, url):
		return urllib2.urlopen(url).read().strip()


def main():
	update = Updater()

if __name__ == '__main__':
	main()
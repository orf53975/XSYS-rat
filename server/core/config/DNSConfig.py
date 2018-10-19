#!/usr/bin/env python3
import os


class DNSConfig:

    def __init__(self):
        self.FreeDNS_URL = None
        self.DNS_ENTRY = None
        self.OLD_IP_FILE = None
        self.USER_KEYS = None

    def init(self):
        self.FreeDNS_URL = 'http://freedns.afraid.org/dynamic/update.php?'
        self.DNS_ENTRY = 'http://ip.dnsexit.com/'
        self.OLD_IP_FILE = os.getcwd() + '/server/resources/ip.old'
        self.USER_KEYS = ["ejUyTlZFd1NVMXVMU2RGZDEzS2d0YUd3OjE3MjI5NDIx", "", ""]
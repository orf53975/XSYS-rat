#!/usr/bin/env python3
import os
import urllib2
from server.core.config.DNSConfig import DNSConfig


class FreeDNSBase(DNSConfig):

    def __init__(self):
        self.init()

    # update the DNS server
    def update_dns(self, ip):
        for key in self.USER_KEYS:
            print("{0}".format(self.url_stripper(self.FreeDNS_URL + key)))
        f = open(self.OLD_IP_FILE, 'w+')
        f.write(ip)
        f.close()

    # start updating ip process
    def start(self):
        new_ip = self.url_stripper(self.DNS_ENTRY)
        if not os.path.exists(self.OLD_IP_FILE):
            self.update_dns(new_ip)
        else:
            f = open(self.OLD_IP_FILE, 'r')
            old_ip = f.read()
            f.close()
            if old_ip != new_ip:
                self.update_dns(new_ip)

    # strip the data from url
    def url_stripper(self, url):
        return self.url_stripper(url)

    # strip the data from url
    @staticmethod
    def url_stripper(url):
        return urllib2.urlopen(url).read().strip()
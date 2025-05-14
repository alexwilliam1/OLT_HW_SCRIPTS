from decouple import config
import os

class Olt_pm(object):
    
    olt_ip = config('OLT_IP')
    username = config('OLT_USER')
    password = config('OLT_PSSWD')
    
    def __init__(self, ip=olt_ip, user=username, passwd=password):
        self.ip = ip
        self.user = user
        self.passwd = passwd
       
    def ip_host(self):
        return self.ip
    
    def user_login(self):
        return self.user
 
    def passwd_login(self):
        return self.passwd

class Olt_bl(object):
    
    olt_ip = config('OLT_IP_BL')
    username = config('OLT_USER_BL')
    password = config('OLT_PSSWD_BL')
    
    def __init__(self, ip=olt_ip, user=username, passwd=password):
        self.ip = ip
        self.user = user
        self.passwd = passwd
       
    def ip_host(self):
        return self.ip
    
    def user_login(self):
        return self.user
 
    def passwd_login(self):
        return self.passwd
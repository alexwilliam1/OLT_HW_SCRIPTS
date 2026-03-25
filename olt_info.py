from decouple import config #pip install python-decouple

class Olt(object):
    
    olt_ip = config('OLT_IP')
    username = config('OLT_USER')
    password = config('OLT_PSSWD')
    olt_name = config('OLT_NAME')
    
    def __init__(self, ip=olt_ip, user=username, passwd=password, name=olt_name):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.name = name
       
    def ip_host(self):
        return self.ip
    
    def user_login(self):
        return self.user
 
    def passwd_login(self):
        return self.passwd
    
    def olt_name(self):
        return self.name

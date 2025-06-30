import paramiko
import time
from olt_info import Olt_ma

olt = Olt_ma()
slot = 1
pon = 3
id = 52

def main():
    ssh = conssh(olt)
    shell = commands(ssh)
    printOutput(shell)
    closeCon(ssh)
    
def conssh(olt):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())        
        return ssh
    except Exception as e:
        print(f"Erro ao conectar a OLT: {e}")
        exit(1)
    
def commands(ssh):
    shell = ssh.invoke_shell()
    shell.send("enable\n")
    shell.send("config\n")
    shell.send(f"interface gpon 0/{slot}\n")
    shell.send(f"display ont optical-info {pon} {id}\n")
    return shell

def printOutput(shell):
    time.sleep(5)  # Aguarda o save completar
    output = shell.recv(65535).decode('utf-8')
    print(output)

def closeCon(ssh):
    ssh.close()

if __name__ == '__main__':
    main()
import paramiko
import time
from olt_info import Olt

olt = Olt()
slot = 2
pon = 6
onu_id = 2
 
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon 0/{slot}\n")
shell.send(f"ont modify {pon} {onu_id} ont-lineprofile-id 321 ont-srvprofile-id 321\n")
shell.send(f"ont port native-vlan {pon} {onu_id} eth 1 vlan 321 priority 0 \n")
shell.send("quit\n")
shell.send(f"undo service-port port 0/{slot}/{pon} ont {onu_id} \n")
shell.send("\n")
shell.send("y\n")
time.sleep(5)
shell.send(f"service-port vlan 321 gpon 0/{slot}/{pon} ont {onu_id} gemport 1 multi-service user-vlan 321 tag-transform translate\n")
shell.send("\n")
time.sleep(5)  

output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
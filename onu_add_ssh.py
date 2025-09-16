import paramiko
import time
from olt_info import Olt
from tqdm import tqdm

olt = Olt() 

# OLT GB
#   "serviceprofile": "100",
#   "lineprofile": "100",
#   "gemport": "100"

slot = 0
pon = 1
vlan = 100 # VLAN PPPOE DA OLT
id = 0 # INITIAL ID
gemport = 100

# BEFORE EXECUTE: CHECK OLT, SLOT, PON AND INITIAL ID
onts = [    
    {"sn": "", "id": id, "desc": "MIGRATION"}, # 1
    {"sn": "", "id": id+1, "desc": "MIGRATION"}, # 2
    {"sn": "", "id": id+2, "desc": "MIGRATION"}, # 3
    {"sn": "", "id": id+3, "desc": "MIGRATION"}, # 4
    {"sn": "", "id": id+4, "desc": "MIGRATION"}, # 5
    {"sn": "", "id": id+5, "desc": "MIGRATION"}, # 6 
    {"sn": "", "id": id+6, "desc": "MIGRATION"}, # 7
    {"sn": "", "id": id+7, "desc": "MIGRATION"}, # 8
    
 ]

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
    print("CONEXÃO ESTABELECIDA COM SUCESSO \n")
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

time.sleep(0.5)
print(f"ENTRANDO NA INTERFACE 0/{slot} \n")
shell.send("enable\n")
time.sleep(0.5)
shell.send("config\n")
time.sleep(0.5)
shell.send(f"interface gpon 0/{slot}\n")
time.sleep(0.5)

# ADD 
for ont in onts:
    print(f"ONT ADD - SN: {ont['sn']}")
    shell.send(f"ont add {pon} {ont['id']} sn-auth {ont['sn']} omci ont-lineprofile-id {vlan} ont-srvprofile-id {vlan} desc \"{ont['desc']}\"\n")
    shell.send("\n")
    time.sleep(0.5)
    
print("\n")
# CONFIGURE NATIVE VLAN
for ont in onts:
    print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
    shell.send(f"ont port native-vlan {pon} {ont['id']} eth 1 vlan {vlan} priority 0\n")
    time.sleep(0.5)

shell.send("quit\n")

print("\n")
# CREATE SERVICE-PORT
for ont in onts:
    print(f"SERVICE-PONT VLAN - SN: {ont['sn']}")
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont['id']} gemport {gemport} multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")  
    time.sleep(0.5)

print("\n")
# SAVE CONFIGS
# shell.send("save\n")
# shell.send("\n")  # CONFIRME THE SAVE COMMAND, IF NECESSARY
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # WAIT SAVE COMPLETE
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")
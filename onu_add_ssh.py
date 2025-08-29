import paramiko
import time
from olt_info import Olt_ma
from tqdm import tqdm

olt = Olt_ma() 

slot = _
pon = _
vlan = 100 # VLAN PPPOE DA OLT
id = _

# BEFORE EXECUTE: CHECK OLT, SLOT, PON AND INITIAL ID
onts = [    
    # {"sn": "", "id": id, "desc": "MIGRATION"}, # 1
    # {"sn": "", "id": id+1, "desc": "MIGRATION"}, # 2
    # {"sn": "", "id": id+2, "desc": "MIGRATION"}, # 3
    # {"sn": "", "id": id+3, "desc": "MIGRATION"}, # 4
    # {"sn": "", "id": id+4, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+5, "desc": "MIGRATION"}, # 6 
    # {"sn": "", "id": id+6, "desc": "MIGRATION"}, # 7
    # {"sn": "", "id": id+7, "desc": "MIGRATION"}, # 8
    # {"sn": "", "id": id+8, "desc": "MIGRATION"}, # 9
    # {"sn": "", "id": id+9, "desc": "MIGRATION"}, # 10
    # {"sn": "", "id": id+10, "desc": "MIGRATION"}, # 11
    # {"sn": "", "id": id+11, "desc": "MIGRATION"}, # 12
    # {"sn": "", "id": id+12, "desc": "MIGRATION"}, # 13
    # {"sn": "", "id": id+13, "desc": "MIGRATION"}, # 14
    # {"sn": "", "id": id+14, "desc": "MIGRATION"}, # 15
    # {"sn": "", "id": id+15, "desc": "MIGRACAO_OLT"}, # 16
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

print(f"ENTRANDO NA INTERFACE 0/{slot} \n")
shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon 0/{slot}\n")

# ADD 
for ont in onts:
    print(f"ONT ADD - SN: {ont['sn']}")
    shell.send(f"ont add {pon} {ont['id']} sn-auth {ont['sn']} omci ont-lineprofile-id {vlan} ont-srvprofile-id {vlan} desc \"{ont['desc']}\"\n")
    shell.send("\n")
    
print("\n")
# CONFIGURE NATIVE VLAN
for ont in onts:
    print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
    shell.send(f"ont port native-vlan {pon} {ont['id']} eth 1 vlan {vlan} priority 0\n")

shell.send("quit\n")

print("\n")
# CREATE SERVICE-PORT
for ont in onts:
    print(f"SERVICE-PONT VLAN - SN: {ont['sn']}")
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont['id']} gemport 2 multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")  

print("\n")
# SAVE CONFIGS
shell.send("save\n")
shell.send("\n")  # CONFIRME THE SAVE COMMAND, IF NECESSARY
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # WAIT SAVE COMPLETE
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")
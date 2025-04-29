import paramiko
import time
from olt_info import Olt_pm
from tqdm import tqdm

olt = Olt_pm()

slot = _
pon = _
vlan = 3000
id = _

# CONFERIR O SLOT, A PON E ID ANTES DE EXECUTAR
onts = [    
    {"sn": "", "id": id, "desc": "MIGRACAO_CTO"}, # 1
    {"sn": "", "id": id+1, "desc": "MIGRACAO_CTO"}, # 2
    {"sn": "", "id": id+2, "desc": "MIGRACAO_CTO"}, # 3
    {"sn": "", "id": id+3, "desc": "MIGRACAO_CTO"}, # 4
    {"sn": "", "id": id+4, "desc": "MIGRACAO_CTO"}, # 5
    {"sn": "", "id": id+5, "desc": "MIGRACAO_CTO"}, # 6 
    {"sn": "", "id": id+6, "desc": "MIGRACAO_CTO"}, # 7
    # {"sn": "", "id": id+7, "desc": "MIGRACAO_CTO"}, # 8
    # {"sn": "", "id": id+8, "desc": "MIGRACAO_CTO"}, # 9
    # {"sn": "", "id": id+9, "desc": "MIGRACAO_CTO"}, # 10
    # {"sn": "", "id": id+10, "desc": "MIGRACAO_CTO"}, # 11
    # {"sn": "", "id": id+11, "desc": "MIGRACAO_CTO"}, # 12
    # {"sn": "", "id": id+12, "desc": "MIGRACAO_CTO"}, # 13
    # {"sn": "", "id": id+13, "desc": "MIGRACAO_CTO"}, # 14
    # {"sn": "", "id": id+14, "desc": "MIGRACAO_CTO"}, # 15
    # {"sn": "", "id": id+15, "desc": "MIGRACAO_CTO"}, # 16
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

# Adicionar 
for ont in onts:
    print(f"ONT ADD - SN: {ont['sn']}")
    shell.send(f"ont add {pon} {ont['id']} sn-auth {ont['sn']} omci ont-lineprofile-id 1 ont-srvprofile-id 1 desc \"{ont['desc']}\"\n")
    shell.send("\n")
    
print("\n")
# Configurar VLAN nativa
for ont in onts:
    print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
    shell.send(f"ont port native-vlan {pon} {ont['id']} eth 1 vlan {vlan} priority 0\n")

shell.send("quit\n")

print("\n")
# Criar service-ports
for ont in onts:
    print(f"SERVICE-PONT VLAN - SN: {ont['sn']}")
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont['id']} gemport 3 multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")  

print("\n")
# Salvar configuração
# print("SALVANDO AS ALTERAÇÕES NA OLT")
shell.send("save\n")
shell.send("\n")  # Responde "Yes" à confirmação, se necessário
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # Aguarda o save completar
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")
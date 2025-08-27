import paramiko #pip install paramiko
import time
from olt_info import Olt_pm
from tqdm import tqdm #pip install tqdm

olt = Olt_pm() 

slot = 3

onts = [    
    {"pon": 10, "id": 2, "desc": "desc"},
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

# EDITAR DESCRIÇÃO DA ONU 
# ont modify pon id desc "desc"
for ont in onts:
    print(f"EDIT DESC ONT: {slot}/{ont['pon']}/{ont['id']}->{ont['desc']}")
    shell.send(f"ont modify {ont['pon']} {ont['id']} desc \"{ont['desc']}\"\n")
    shell.send("\n")

shell.send("quit\n")

# print("\n")
# print("SALVANDO AS ALTERAÇÕES NA OLT")
shell.send("save\n")
shell.send("\n")  # Responde "Yes" à confirmação, se necessário
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # Aguarda o save completar
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")
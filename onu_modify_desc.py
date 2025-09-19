import paramiko #pip install paramiko
import time
from olt_info import Olt
from tqdm import tqdm #pip install tqdm

olt = Olt() 

slot = 1
pon = 5

onts = [
{"id": 17, "desc": ""},
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
shell.send(" \n")
time.sleep(0.5)
shell.send("enable\n")
time.sleep(0.5)
shell.send("config\n")
time.sleep(0.5)
shell.send(f"interface gpon 0/{slot}\n")
time.sleep(0.5)

# EDIT ONU DESCRIPTION
# ont modify pon id desc "desc"
for ont in onts:
    print(f"EDIT DESC ONT: {slot}/{pon}/{ont['id']}->{ont['desc']}")
    shell.send(f"ont modify {pon} {ont['id']} desc \"{ont['desc']}\"\n")
    time.sleep(0.5)
    # shell.send("\n")

shell.send("quit\n")

# shell.send("save\n")
# shell.send("\n") # CONFIRM THE SAVE COMMAND, IF NECESSARY
for _ in tqdm(range(50), desc="WAIT..."):
        time.sleep(1)  # WAIT EXECUTION
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")
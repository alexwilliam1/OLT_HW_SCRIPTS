import paramiko
import time
from olt_info import Olt_ma
from tqdm import tqdm

olt = Olt_ma()
frame = 0          
slot = 1             
pon = 0                    

# ONT IDS LIST
ont_ids_to_remove = [54, 51, 50, 53, 52, 48, 49]  

# SSH CONNECTION
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

# ENTER GPON INTERFACE
shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon {frame}/{slot}\n")

for ont_id in ont_ids_to_remove:
    shell.send(f"ont delete {pon} {ont_id}\n")
    time.sleep(0.5)  # PAUSE BETWEEN COMMANDS TO AVOID OVERLOAD

# EXIT CONFG MODE
shell.send("quit\n")
shell.send("save\n")
shell.send("\n")  # CONFIRM THE SAVE COMMAND, IF NECESSARY
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # WAIT SAVING


output = shell.recv(65535).decode('utf-8')
print("Saída da OLT:")
print(output)

ssh.close()

print(f"Remoção das ONUs {ont_ids_to_remove} - 0/{slot}/{pon} concluída.")
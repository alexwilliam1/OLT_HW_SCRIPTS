import paramiko
import time
from olt_info import Olt
from tqdm import tqdm

olt = Olt()          
slot = 1           
pon = 8                

# ONT IDS LIST
ont_ids_to_remove = [41, 37, 60, 3, 53, 33, 54, 28, 8, 26, 39, 44, 66, 35, 62, 68, 18, 14, 38, 46, 22, 23, 25]  

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
time.sleep(0.5)
shell.send("\n")
time.sleep(0.5)
shell.send("enable\n")
time.sleep(0.5)
shell.send("config\n")
time.sleep(0.5)

for ont_id in ont_ids_to_remove:
    shell.send(f"undo service-port port 0/{slot}/{pon} ont {ont_id}\n")
    time.sleep(0.5)
    shell.send("\n")
    time.sleep(0.5)
    shell.send("y\n")
    time.sleep(0.5)

shell.send(f"interface gpon 0/{slot}\n")
time.sleep(0.5)

for ont_id in ont_ids_to_remove:
    shell.send(f"ont delete {pon} {ont_id}\n")
    time.sleep(0.5)  # PAUSE BETWEEN COMMANDS TO AVOID OVERLOAD

# EXIT CONFG MODE
# shell.send("quit\n")
# shell.send("save\n")
# shell.send("\n")  # CONFIRM THE SAVE COMMAND, IF NECESSARY
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # WAIT SAVING


output = shell.recv(65535).decode('utf-8')
print("Saída da OLT:")
print(output)

ssh.close()

print(f"Remoção das ONUs {ont_ids_to_remove} - 0/{slot}/{pon} concluída.")
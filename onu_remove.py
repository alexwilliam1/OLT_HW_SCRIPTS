import paramiko
import time
from olt_info import Olt
from tqdm import tqdm

olt = Olt()
frame = 0          
slot = 0             
pon = 2                    

# ONT IDS LIST
ont_ids_to_remove = [19, 8, 9, 4, 5, 6, 7, 0, 1, 2, 3, 24, 21, 20, 23, 22, 18, 14, 15, 16, 17, 10, 11, 12, 13]  

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

for ont_id in ont_ids_to_remove:
    shell.send(f"undo service-port port {frame}/{slot}/{pon} ont {ont_id}\n")
    time.sleep(0.5)

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

print(f"Remoção das ONUs {ont_ids_to_remove} - {frame}/{slot}/{pon} concluída.")
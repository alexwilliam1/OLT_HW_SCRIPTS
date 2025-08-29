import paramiko
import time
import re
from olt_info import Olt_pm

olt = Olt_pm()
frame = 0
slot = 1
pon = 3
ont_id = 52  # ONT ID

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

shell.send("enable\n")
shell.send(f"display mac-address ont {frame}/{slot}/{pon} {ont_id}\n")
shell.send("\n")
time.sleep(2)

output = shell.recv(65535).decode('utf-8')
ssh.close()

# EXTRACT MAC ADDRESSES USING REGEX
macs = re.findall(r"([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})", output)

if macs:
    print(f"MACs associados à ONU {ont_id} na PON {frame}/{slot}/{pon}:")
    for mac in macs:
        print(mac)
else:
    print("Nenhum MAC encontrado.")
    print("Saída bruta:", output)
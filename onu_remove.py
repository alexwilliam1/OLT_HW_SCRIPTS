import time
from olt_info import Olt
from olt_ssh import connect, enter_config, recv_output, disconnect

olt = Olt()
slot = _
pon = _

# ONT IDS LIST
ont_ids_to_remove = [
]

ssh, shell = connect(olt)
enter_config(shell, slot=None)

for ont_id in ont_ids_to_remove:
    shell.send(f"undo service-port port 0/{slot}/{pon} ont {ont_id}\n")
    time.sleep(0.5)
    shell.send("\n")
    time.sleep(0.5)
    shell.send("y\n")
    time.sleep(0.5)

enter_config(shell, slot=slot)

for ont_id in ont_ids_to_remove:
    shell.send(f"ont delete {pon} {ont_id}\n")
    time.sleep(0.5)

output = recv_output(shell, delay=5)
print("Saida da OLT:")
print(output)
disconnect(ssh)

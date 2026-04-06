import time
from olt_info import Olt
from olt_ssh import connect, enter_config, recv_output, save_config, disconnect
from tqdm import tqdm

olt = Olt()

olt_name = olt.olt_name()
slot = _
pon = _

onts = [
    {"id": 0, "desc": "desc"},
]

ssh, shell = connect(olt)
print(f"{olt_name} - SLOT 0/{slot} PON {pon} \n")
enter_config(shell, slot=slot)

# EDIT ONU DESCRIPTION
# ont modify pon id desc "desc"
for ont in tqdm(onts, desc="EDITING DESC"):
    print(f"EDIT DESC ONT: {slot}/{pon}/{ont['id']}->{ont['desc']}")
    shell.send(f"ont modify {pon} {ont['id']} desc \"{ont['desc']}\"\n")
    time.sleep(0.5)

shell.send("quit\n")
save_config(shell, show_progress=True)
disconnect(ssh)

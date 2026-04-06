import time
from olt_info import Olt
from olt_ssh import connect, enter_config, recv_output, disconnect

olt = Olt()
slot = _
pon = _
onu_id = _

ssh, shell = connect(olt)
enter_config(shell, slot=slot)
shell.send(f"ont modify {pon} {onu_id} ont-lineprofile-id 321 ont-srvprofile-id 321\n")
shell.send(f"ont port native-vlan {pon} {onu_id} eth 1 vlan 321 priority 0 \n")
shell.send("quit\n")
shell.send(f"undo service-port port 0/{slot}/{pon} ont {onu_id} \n")
shell.send("\n")
shell.send("y\n")
time.sleep(5)
shell.send(f"service-port vlan 321 gpon 0/{slot}/{pon} ont {onu_id} gemport 1 multi-service user-vlan 321 tag-transform translate\n")
shell.send("\n")
time.sleep(5)  

output = recv_output(shell, delay=5)
print(output)
disconnect(ssh)
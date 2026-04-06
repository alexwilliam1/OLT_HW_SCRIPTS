from olt_info import Olt
from olt_ssh import connect, enter_config, recv_output, disconnect

olt = Olt()
slot = _
pon = _
onu_id = _

ssh, shell = connect(olt)
enter_config(shell, slot=slot)
shell.send(f"display ont port state {pon} {onu_id} eth-port all \n")
print(recv_output(shell))
disconnect(ssh)

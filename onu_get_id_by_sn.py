from olt_info import Olt
from olt_ssh import connect, recv_output, disconnect

olt = Olt()

ssh, shell = connect(olt)
shell.send("enable\n")
shell.send("config\n")
shell.send(f"display ont info by-sn HWTC3203D0BC \n")
print(recv_output(shell))
disconnect(ssh)


import re
from olt_info import Olt
from olt_ssh import connect, recv_output, disconnect

olt = Olt()
slot = 2
pon = 4
ont_id = 38  # ONT ID

ssh, shell = connect(olt)
shell.send("enable\n")
shell.send(f"display mac-address port 0/{slot}/{pon} ont {ont_id}\n")
shell.send("\n")
output = recv_output(shell, delay=2)
disconnect(ssh, msg=False)

# EXTRACT MAC ADDRESSES USING REGEX
macs = re.findall(r"([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})", output)

if macs:
    print(f"MACs associados à ONU {ont_id} na PON 0/{slot}/{pon}:")
    for mac in macs:
        print(mac)
else:
    print("Nenhum MAC encontrado.")
    print("Saída bruta:", output)
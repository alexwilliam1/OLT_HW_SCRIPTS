import time
from olt_info import Olt
from olt_ssh import connect, enter_config, disconnect
from tqdm import tqdm

olt = Olt()

slot = _
pon = _
vlan = _ # VLAN PPPOE DA OLT
id = _ # INITIAL ID
gemport = _

# BEFORE EXECUTE: CHECK OLT, SLOT, PON AND INITIAL ID
onts = [    
    # {"sn": "", "id": id, "desc": "MIGRATION"}, # 1
    # {"sn": "", "id": id+1, "desc": "MIGRATION"}, # 2
    # {"sn": "", "id": id+2, "desc": "MIGRATION"}, # 3 
    # {"sn": "", "id": id+3, "desc": "MIGRATION"}, # 4
    # {"sn": "", "id": id+4, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+5, "desc": "MIGRATION"}, # 6 
    # {"sn": "", "id": id+6, "desc": "MIGRATION"}, # 7
    # {"sn": "", "id": id+7, "desc": "MIGRATION"}, # 8
    # {"sn": "", "id": id+8, "desc": "MIGRATION"}, # 1
    # {"sn": "", "id": id+9, "desc": "MIGRATION"}, # 2
    # {"sn": "", "id": id+10, "desc": "MIGRATION"}, # 3
    # {"sn": "", "id": id+11, "desc": "MIGRATION"}, # 4
    # {"sn": "", "id": id+12, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+13, "desc": "MIGRATION"}, # 6 
    # {"sn": "", "id": id+14, "desc": "MIGRATION"}, # 7
    # {"sn": "", "id": id+15, "desc": "MIGRATION"}, # 8
    # {"sn": "", "id": id+16, "desc": "MIGRATION"}, # 1
    # {"sn": "", "id": id+17, "desc": "MIGRATION"}, # 3
    # {"sn": "", "id": id+18, "desc": "MIGRATION"}, # 4
    # {"sn": "", "id": id+19, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+20, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+21, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+22, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+23, "desc": "MIGRATION"}, # 5
    # {"sn": "", "id": id+24, "desc": "MIGRATION"}, # 5
 ]

ssh, shell = connect(olt)
print("CONEXÃO ESTABELECIDA COM SUCESSO \n")
print(f"ENTRANDO NA INTERFACE 0/{slot} \n")
enter_config(shell, slot=slot)

# ADD 
for ont in onts:
    print(f"ONT ADD - SN: {ont['sn']}")
    shell.send(f"ont add {pon} {ont['id']} sn-auth {ont['sn']} omci ont-lineprofile-id {vlan} ont-srvprofile-id {vlan} desc \"{ont['desc']}\"\n")
    shell.send("\n")
    time.sleep(0.5)
    
print("\n")
# CONFIGURE NATIVE VLAN
for ont in onts:
    print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
    shell.send(f"ont port native-vlan {pon} {ont['id']} eth 1 vlan {vlan} priority 0\n")
    time.sleep(0.5)

shell.send("quit\n")

print("\n")
# CREATE SERVICE-PORT
for ont in onts:
    print(f"SERVICE-PONT VLAN - SN: {ont['sn']}")
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont['id']} gemport {gemport} multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")  
    time.sleep(0.5)

print("\n")
# SAVE CONFIGS
save_config(shell, show_progress=True)
disconnect(ssh)
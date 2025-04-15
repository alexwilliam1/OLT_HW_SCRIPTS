import paramiko
import time
from olt_info import Olt_pm
from tqdm import tqdm

def conssh(olt):
    print("ESTABELECENDO CONEXÃO COM A OLT...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
        print("CONEXÃO ESTABELECIDA COM SUCESSO.")
        return ssh
    except Exception as e:
        print(f"Erro ao conectar a OLT: {e}")
        exit(1)

def enter_inter(ssh, slot):
    print(f"ENTRANDO NA INTERFACE 0/{slot}...")
    shell = ssh.invoke_shell()
    shell.send("enable\n")
    shell.send("config\n")
    shell.send(f"interface gpon 0/{slot}\n")
    return shell
    
def ont_add(shell, pon, ont_id, ont_sn, ont_desc):
    shell.send(f"ont add {pon} {ont_id} sn-auth {ont_sn} omci ont-lineprofile-id 1 ont-srvprofile-id 1 desc \"{ont_desc}\"\n")
    shell.send("\n")

def ont_port_native_vlan(shell, pon, ont_id, vlan):
    shell.send(f"ont port native-vlan {pon} {ont_id} eth 1 vlan {vlan} priority 0\n")

def quit(shell):
    shell.send("quit\n")

def ont_srv_port(shell, slot, pon, vlan, ont_id):
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont_id} gemport 3 multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")

def olt_save(shell):
    shell.send("save\n")
    shell.send("\n")  # Responde "Yes" à confirmação, se necessário
    for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT..."):
        time.sleep(1)  # Aguarda o save completar
    
def printOutput(shell):
    output = shell.recv(65535).decode('utf-8')
    print(output)

def closeCon(ssh):
    ssh.close()
    
def main():
    onts = [
        {"sn": "", "id": 30, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 31, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 32, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 33, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 34, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 35, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 36, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 37, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
        {"sn": "", "id": 38, "desc": "MIGRACAO_CTO"},
    ]

    slot = 1    
    pon = 14
    vlan = 3000
    
    olt = Olt_pm()
    
    ssh = conssh(olt)
    shell = enter_inter(ssh, slot)
    
    for ont in tqdm(onts, desc="SUBINDO ONUS..."):
        # print(f"AUTORIZANDO ONU: {ont['sn']}")
        ont_add(shell, pon, ont['id'], ont['sn'], ont['desc'])
        ont_port_native_vlan(shell, pon, ont['id'], vlan)
        quit(shell)
        ont_srv_port(shell, slot, pon, vlan, ont['id'])
    
    olt_save(shell)
    printOutput(shell)
    print("FECHANDO A CONEXÃO COM A OLT...\n")
    closeCon(ssh)
    print("PROCESSO CONCLUIDO COM SUCESSO\n")
        
if __name__ == '__main__':
    main()
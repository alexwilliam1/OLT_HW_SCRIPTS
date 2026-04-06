import paramiko
import time
from olt_info import Olt


def connect(olt=None):
    """Open SSH session to OLT and return (ssh, shell) tuple."""
    if olt is None:
        olt = Olt()
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
        shell = ssh.invoke_shell()
        return ssh, shell
    except Exception as e:
        print(f"Erro ao conectar a OLT: {e}")
        exit(1)


def enter_config(shell, slot=None):
    """Enter enable + config mode, optionally enter a GPON interface."""
    shell.send("enable\n")
    time.sleep(0.3)
    shell.send("config\n")
    time.sleep(0.3)
    if slot is not None:
        shell.send(f"interface gpon 0/{slot}\n")
        time.sleep(0.3)


def recv_output(shell, delay=5):
    """Wait and read shell output."""
    time.sleep(delay)
    return shell.recv(65535).decode("utf-8")


def save_config(shell, show_progress=True):
    """Save OLT configuration and wait for completion."""
    shell.send("save\n")
    time.sleep(0.5)
    shell.send("\n")
    if show_progress:
        from tqdm import tqdm
        for _ in tqdm(range(120), desc="SALVANDO AS ALTERACOES NA OLT"):
            time.sleep(1)
    print(recv_output(shell, delay=5))


def disconnect(ssh, msg=True):
    """Close SSH connection."""
    ssh.close()
    if msg:
        print("PROCESSO FINALIZADO.\nCONEXAO COM A OLT FECHADA.")

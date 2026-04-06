from netmiko import ConnectHandler, NetmikoTimeoutException
from olt_info import Olt


def connect(olt=None, protocol='ssh'):
    if olt is None:
        olt = Olt()

    device = {
        'device_type': 'terminal_server',
        'host': olt.ip_host(),
        'username': olt.user_login(),
        'password': olt.passwd_login(),
    }

    if protocol == 'ssh':
        device['port'] = 22
        device['transport'] = 'ssh'
    else:
        device['port'] = 23341
        device['transport'] = 'telnet'

    try:
        conn = ConnectHandler(**device)
        if protocol == 'ssh':
            conn.send_command_timing('screen-length 0 temporary')
        print(f"CONEXAO ESTABELECIDA COM SUCESSO via {protocol.upper()} \n")
        return conn
    except NetmikoTimeoutException as e:
        print(f"Erro ao conectar a OLT via {protocol}: {e}")
        exit(1)
    except Exception as e:
        print(f"Erro inesperado ao conectar a OLT: {e}")
        exit(1)


def send_command(conn, cmd):
    return conn.send_command_timing(cmd, strip_prompt=False, strip_command=False)


def send_commands(conn, commands):
    return conn.send_config_set(commands)


def disconnect(conn, msg=True):
    conn.disconnect()
    if msg:
        print("PROCESSO FINALIZADO.\nCONEXAO COM A OLT FECHADA.")

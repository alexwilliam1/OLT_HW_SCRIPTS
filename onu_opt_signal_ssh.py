from olt_info import Olt
from olt_ssh import connect, enter_config, recv_output, disconnect

olt = Olt()
slot = 1
pon = 0
id = 98

def main():
    ssh, shell = connect(olt)
    enter_config(shell, slot=slot)
    shell.send(f"display ont optical-info {pon} {id}\n")
    print(recv_output(shell))
    disconnect(ssh)

if __name__ == '__main__':
    main()

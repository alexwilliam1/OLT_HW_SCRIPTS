import time
from netmiko import ConnectHandler
from olt_info import Olt

# --- CONFIG ---
protocol = 'telnet'  # 'ssh' ou 'telnet'
port = _         # porta telnet
slot = _             # slot GPON
pon = _              # porta PON
vlan = _          # VLAN PPPoE da OLT
id = _              # ID inicial
gemport = _          # Gemport
line_srv = _        # Line/Srv profile
# --------------

# ONTS TO ADD (fill SNs before running)
onts_add = [
    # {"sn": "SN", "id": id, "desc": "MIGRATION"}, # 1
    # {"sn": "SN", "id": id+1, "desc": "MIGRATION"}, # 2
]

# ONT IDS TO REMOVE
ont_ids_to_remove = [
    # 12
]

# ONTS TO MODIFY DESCRIPTION
onts_to_modify = [
    # {"id": 0, "desc": "desc"},
]


class ModifyOnt:
    """Modify ONU descriptions via Telnet with Netmiko."""

    def __init__(self):
        olt = Olt()
        self.conn = ConnectHandler(
            device_type='huawei_olt_telnet',
            host=olt.ip_host(),
            username=olt.user_login(),
            password=olt.passwd_login(),
            port=port,
        )
        print("CONEXAO ESTABELECIDA COM SUCESSO\n")

    def run(self):
        conn = self.conn
        conn.send_command_timing('enable')
        conn.send_command_timing('config')
        conn.send_command_timing(f'interface gpon 0/{slot}')

        for ont in onts_to_modify:
            print(f"ONT MODIFY DESC - PON {slot}/{pon}/{ont['id']} -> {ont['desc']}")
            ret = conn.send_command_timing(
                f'ont modify {pon} {ont["id"]} desc "{ont["desc"]}"'
            )
            if ret:
                print(f"  >> {ret.strip()}")

        conn.send_command_timing('quit')
        print()
        return self

    def finish(self):
        self.conn.disconnect()
        print("PROCESSO FINALIZADO.\nCONEXAO COM A OLT FECHADA.")
        return self


class AddOnt:
    """Add ONUs with native-vlan and service-port config via Netmiko."""

    def __init__(self):
        olt = Olt()
        self.conn = ConnectHandler(
            device_type='huawei_olt_telnet',
            host=olt.ip_host(),
            username=olt.user_login(),
            password=olt.passwd_login(),
            port=port,
        )
        print("CONEXAO ESTABELECIDA COM SUCESSO\n")

    def run(self):
        conn = self.conn
        conn.send_command_timing('enable')
        conn.send_command_timing('config')
        conn.send_command_timing(f'interface gpon 0/{slot}')

        # ADD ONTs
        for ont in onts_add:
            print(f"ONT ADD - SN: {ont['sn']}")
            ret = conn.send_command_timing(
                f'ont add {pon} {ont["id"]} sn-auth {ont["sn"]} '
                f'omci ont-lineprofile-id {line_srv} ont-srvprofile-id {line_srv} '
                f'desc "{ont["desc"]}"'
            )
            if ret:
                print(f"  >> {ret.strip()}")

        print()

        # CONFIGURE NATIVE VLAN
        for ont in onts_add:
            print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
            ret = conn.send_command_timing(
                f'ont port native-vlan {pon} {ont["id"]} eth 1 '
                f'vlan {vlan} priority 0'
            )
            if ret:
                print(f"  >> {ret.strip()}")

        conn.send_command_timing('quit')

        print()

        # CREATE SERVICE-PORT
        for ont in onts_add:
            print(f"SERVICE-PORT VLAN - SN: {ont['sn']}")
            ret = conn.send_command_timing(
                f'service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont["id"]} '
                f'gemport {gemport} multi-service user-vlan {vlan} '
                f'tag-transform translate'
            )
            if ret:
                print(f"  >> {ret.strip()}")

        print()
        return self

    def finish(self):
        self.conn.disconnect()
        print("PROCESSO FINALIZADO.\nCONEXAO COM A OLT FECHADA.")
        return self


class RemoveOnt:
    """Remove ONUs and their service-ports via Netmiko."""

    def __init__(self):
        olt = Olt()
        self.conn = ConnectHandler(
            device_type='huawei_olt_telnet',
            host=olt.ip_host(),
            username=olt.user_login(),
            password=olt.passwd_login(),
            port=port,
        )
        print("CONEXAO ESTABELECIDA COM SUCESSO\n")

    def run(self):
        conn = self.conn
        conn.send_command_timing('enable')
        conn.send_command_timing('config')

        # UNDO SERVICE-PORT
        for ont_id in ont_ids_to_remove:
            print(f"UNDO SERVICE-PORT - ONT ID: {ont_id}")
            ret = conn.send_command_timing(
                f'undo service-port port 0/{slot}/{pon} ont {ont_id}'
            )
            if ret:
                print(f"  >> {ret.strip()}")
            # Confirm if prompted
            ret = conn.send_command_timing('y')
            if ret:
                print(f"  >> {ret.strip()}")

        # ENTER GPON INTERFACE
        conn.send_command_timing(f'interface gpon 0/{slot}')

        # DELETE ONTs
        for ont_id in ont_ids_to_remove:
            print(f"ONT DELETE - ID: {ont_id}")
            ret = conn.send_command_timing(f'ont delete {pon} {ont_id}')
            if ret:
                print(f"  >> {ret.strip()}")

        print()
        return self

    def finish(self):
        self.conn.disconnect()
        print("PROCESSO FINALIZADO.\nCONEXAO COM A OLT FECHADA.")
        return self


def main():
    # ADD onts
    # AddOnt().run().finish()

    # REMOVE onts
    # RemoveOnt().run().finish()
    
    # MODIFY onts
    ModifyOnt().run().finish()


if __name__ == '__main__':
    main()

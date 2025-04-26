from olt_info import Olt_pm
from tqdm import tqdm

olt = Olt_pm()

slot = 1
pon = 15
vlan = 3000
id = 10

onts = [    
    {"sn": "", "id": id, "desc": "MIGRACAO_CTO"}, # 1
    {"sn": "", "id": id+1, "desc": "MIGRACAO_CTO"}, # 2
    {"sn": "", "id": id+2, "desc": "MIGRACAO_CTO"}, # 3
    {"sn": "", "id": id+3, "desc": "MIGRACAO_CTO"}, # 4
    {"sn": "", "id": id+4, "desc": "MIGRACAO_CTO"}, # 5
    {"sn": "", "id": id+5, "desc": "MIGRACAO_CTO"}, # 6 
    # {"sn": "", "id": id+6, "desc": "MIGRACAO_CTO"}, # 7
    # {"sn": "", "id": id+7, "desc": "MIGRACAO_CTO"}, # 8
    # {"sn": "", "id": id+8, "desc": "MIGRACAO_CTO"}, # 9
    # {"sn": "", "id": id+9, "desc": "MIGRACAO_CTO"}, # 10
    # {"sn": "", "id": id+10, "desc": "MIGRACAO_CTO"}, # 11
    # {"sn": "", "id": id+11, "desc": "MIGRACAO_CTO"}, # 12
    # {"sn": "", "id": id+12, "desc": "MIGRACAO_CTO"}, # 13
    # {"sn": "", "id": id+13, "desc": "MIGRACAO_CTO"}, # 14
    # {"sn": "", "id": id+14, "desc": "MIGRACAO_CTO"}, # 15
    # {"sn": "", "id": id+15, "desc": "MIGRACAO_CTO"}, # 16
]

def main():
    for ont in onts:
        print(f"{ont['id']}")
    # for ont in tqdm(onts, desc="ONT ADD"):
    #     print(f"{ont['id']}")
    #     pass
    # print(olt.ip_host(), olt.user_login(), olt.passwd_login())

def prt(sn):
    print(sn)

if __name__ == '__main__':
    main()
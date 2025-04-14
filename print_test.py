from olt_info import Olt_pm
from tqdm import tqdm

olt = Olt_pm()

onts = [    
    {"sn": "1", "id": 22, "desc": "MIGRACAO_CTO"},
    {"sn": "2", "id": 23, "desc": "MIGRACAO_CTO"},
    {"sn": "3", "id": 24, "desc": "MIGRACAO_CTO"},
    {"sn": "4", "id": 25, "desc": "MIGRACAO_CTO"},
    {"sn": "5", "id": 26, "desc": "MIGRACAO_CTO"},
    {"sn": "6", "id": 27, "desc": "MIGRACAO_CTO"},
    {"sn": "7", "id": 28, "desc": "MIGRACAO_CTO"},
    {"sn": "8", "id": 29, "desc": "MIGRACAO_CTO"},
]


def main():
    # for ont in tqdm(onts, desc="ONT ADD"):
    #     # print(f"{ont['id']}")
    #     pass
    print(olt.ip_host(), olt.user_login(), olt.passwd_login())

def prt(sn):
    print(sn)

if __name__ == '__main__':
    main()
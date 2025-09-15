from olt_info import Olt
from tqdm import tqdm

olt = Olt()

slot = 1
pon = 15
vlan = 3000
id = 10

onts = [    
    {"sn": "", "id": id, "desc": "TESTS"}, # 1
    {"sn": "", "id": id+1, "desc": "TESTS"}, # 2
    {"sn": "", "id": id+2, "desc": "TESTS"}, # 3
    {"sn": "", "id": id+3, "desc": "TESTS"}, # 4
    {"sn": "", "id": id+4, "desc": "TESTS"}, # 5
    {"sn": "", "id": id+5, "desc": "TESTS"}, # 6 
    # {"sn": "", "id": id+6, "desc": "TESTS"}, # 7
    # {"sn": "", "id": id+7, "desc": "TESTS"}, # 8
    # {"sn": "", "id": id+8, "desc": "TESTS"}, # 9
    # {"sn": "", "id": id+9, "desc": "TESTS"}, # 10
    # {"sn": "", "id": id+10, "desc": "TESTS"}, # 11
    # {"sn": "", "id": id+11, "desc": "TESTS"}, # 12
    # {"sn": "", "id": id+12, "desc": "TESTS"}, # 13
    # {"sn": "", "id": id+13, "desc": "TESTS"}, # 14
    # {"sn": "", "id": id+14, "desc": "TESTS"}, # 15
    # {"sn": "", "id": id+15, "desc": "TESTS"}, # 16
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
import paramiko
import time
from olt_info import Olt_pm
from tqdm import tqdm

olt = Olt_pm()
frame = 0          
slot = 1             
pon = 15                    

# Lista de IDs das ONUs a serem removidas
ont_ids_to_remove = [54, 51, 50, 53, 52, 48, 49]  # Substitua pelos IDs reais que deseja remover

# Conectar à OLT via SSH
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)
    
# Enviar comandos para entrar no modo GPON
shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon {frame}/{slot}\n")

# Remover cada ONU da lista
for ont_id in ont_ids_to_remove:
    shell.send(f"ont delete {pon} {ont_id}\n")
    time.sleep(0.5)  # Pequena pausa entre comandos para evitar sobrecarga

# Sair do modo GPON e salvar configuração
shell.send("quit\n")
shell.send("save\n")
shell.send("\n")  # Confirmação do save, se necessário
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # Aguarda o save completar

# Capturar e exibir a saída para verificação
output = shell.recv(65535).decode('utf-8')
print("Saída da OLT:")
print(output)

# Fechar a conexão
ssh.close()

print(f"Remoção das ONUs {ont_ids_to_remove} na PON 0/{slot}/{pon} concluída.")
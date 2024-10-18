from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import os

# Definindo os paths para os arquivos e diretórios do projeto

code_path = os.path.dirname(os.path.abspath(__file__))
files_path = os.path.join(code_path, "files")
users_path = os.path.join(code_path, "users.txt")

# Carregando a lista dos usuários

with open(users_path, "r") as file:
    users = file.read()
    
users = users.split("\n") #OBS: DEVE SER CASE SENSITIVE

# Inicializa socket servidor

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', 11550))

serverSocket.listen(1)

print("Servidor em operação...")

# Busca conexões a serem aceitas

state = "waiting"

while 1:
        try:
            if state == "waiting":
                connectionSocket, address = serverSocket.accept()
                message = connectionSocket.recv(1024).decode()
                
                seq = ""
                command = ""
                args = ""
                
                try:
                    seq, command, args = message.split(" ", 2)
                    
                    seq_num_validation = int(seq)
                    
                except:
                    connectionSocket.send(f"0 NOK".encode())   # [SEQ] NOK
                    connectionSocket.close()
                    continue
                
                # Comando CUMP
                # Recebe [SEQ_NUM][COMMAND][ARGS]
                if command != "CUMP" or args not in users:
                    connectionSocket.send(f"{seq} NOK".encode())   # [SEQ] NOK
                    connectionSocket.close()
                    
                else:
                    connectionSocket.send(f"{seq} OK".encode())    # [SEQ] OK
                    state = "ready"
            
            elif state == "ready":
                message = connectionSocket.recv(1024).decode()
                
                # Obtenção de [sequência][comando] possível [args]
                try:
                    #breakpoint()
                    seq, command, args = message.split(" ", 2)
                    
                    seq_num_validation = int(seq)
                    
                    if args == "":
                        raise ValueError
                    
                except:
                    try:
                        seq, command = message.split(" ", 1)
                        
                        seq_num_validation = int(seq)
                    
                    # Caso a mensagem não esteja nos padrões informados, retorna um NOK.
                    except:
                        connectionSocket.send(f"0 NOK".encode())   # [SEQ] NOK
                        continue
                    
                if command == "LIST":
                    # Comando LIST
                    # Recebe [SEQ_NUM][COMMAND]        <=> <seq> LIST
                    # Retorna [SEQ_NUM][REPLY][ARGS]   <=> <seq> ARQS <num> nome1,nome2,nome3,... | <seq> NOK
                    try:
                        files_list = os.listdir(files_path)
                        num = len(files_list)
                        arqs = ",".join(files_list)
                        connectionSocket.send(f"{seq} ARQS {num} {arqs}".encode())   # [SEQ] ARQS <num> nome1,nome2,nome3...
                    except:
                        connectionSocket.send(f"{seq} NOK".encode())   # [SEQ] NOK
                    
                elif command == "PEGA":
                    # Comando PEGA
                    # Recebe  [SEQ_NUM][COMMAND][ARGS] <=> <seq> PEGA <nome>
                    # Retorna [SEQ_NUM][REPLY][ARGS]   <=> <seq> ARQ <tam> <dados> | <seq> NOK
                    #breakpoint()
                    
                    try:
                        if args in os.listdir(files_path):
                            size = os.path.getsize(f"{files_path}/{args}")
                            
                            with open(f"{files_path}/{args}", "rb") as file:
                                data = file.read()
                            
                            connectionSocket.send(f"{seq} ARQ {size} {data}".encode())   # [SEQ] ARQ <tam> <dados>
                        else:
                            raise FileNotFoundError
                    except:
                        connectionSocket.send(f"{seq} NOK".encode())   # [SEQ] NOK
                
                elif command == "TERM":
                    # Comando TERM
                    # Recebe  [SEQ_NUM][COMMAND]       <=> <seq> TERM
                    # Retorna [SEQ_NUM][REPLY]         <=> <seq> OK | <seq> NOK
                    try:
                        state = "waiting"
                        connectionSocket.send(f"{seq} OK".encode())   # [SEQ] OK
                        connectionSocket.close()
                    except:
                        connectionSocket.send(f"{seq} NOK".encode())   # [SEQ] NOK
                
                # Quaisquer outro comando identificado que não seja os configurados neste servidor.
                else:
                    connectionSocket.send(f"{seq} NOK".encode())   # [SEQ] NOK

        except (KeyboardInterrupt, SystemExit):
            serverSocket.shutdown(SHUT_RDWR)
            break
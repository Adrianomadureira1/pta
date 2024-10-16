import random, os
import pytest
from socket import socket, AF_INET, SOCK_STREAM

@pytest.fixture(params=[{"file": "dummyfile09-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile10-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile01-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile16-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile12-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile11-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile06-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile14-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile07-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile08-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile13-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile05-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile15-with-a-bigger-name-to-test-your-buffer-treatment.txt"},
                        {"file": "dummyfile02-with-a-bigger-name-to-test-your-buffer-treatment.txt"}, # Arquivo "grande"
                        {"file": "dummyfile04-with-a-bigger-name-to-test-your-buffer-treatment.txt"}, # Arquivo "grande"
                        {"file": "dummyfile03-with-a-bigger-name-to-test-your-buffer-treatment.png"}, # Arquivo "grande"
                        ])
def pega_param(request):
    yield request.param

@pytest.fixture(scope="function")
def client_socket():
    server_name = "127.0.0.1"
    server_port = 11550

    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Conexão do cliente com servidor

    clientSocket.connect((server_name, server_port))
    
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "CUMP"
    args = "user1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    clientSocket.send(message.encode("ascii"))
    
    returned_message, addr = clientSocket.recvfrom(2048)

    yield clientSocket
       
def test_good_pega(client_socket, pega_param):
    """Teste fim-a-fim do PEGA em um caminho 'feliz'."""   
    # Constrói uma mensagem
    
    files_dir = "files"
    
    file_path = pega_param["file"]

    seq_num = random.randint(1, 10000)
    command = "PEGA"

    message = f"{seq_num} {command} {file_path}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    size = os.path.getsize(f"pta-server/{files_dir}/{file_path}")
    
    with open(f"./pta-server/{files_dir}/{file_path}", "rb") as file:
        file_content = file.read()
    
    if file_path.split(".")[1] == "png": # Verifica se a extensão do arquivo é PNG, se for, ela já vem codificada em bytes.
        expected_message = f"{seq_num} ARQ {size} ".encode("ascii") + file_content
    else:
        expected_message = f"{seq_num} ARQ {size} {file_content}".encode("ascii")   # [SEQ] ARQ <tam> <dados>

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(8182)
    
    assert expected_message == returned_message
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_pega(client_socket):
    """Teste do PEGA para um arquivo que não existe."""   
    # Constrói uma mensagem
       
    file_path = "blablabla"

    seq_num = random.randint(1, 10000)
    command = "PEGA"

    message = f"{seq_num} {command} {file_path}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} NOK".encode("ascii")
    
    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(8182)
    
    assert expected_message == returned_message
    
    client_socket.send(f"0 TERM".encode("ascii"))
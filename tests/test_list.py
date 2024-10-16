import random
import pytest
from socket import socket, AF_INET, SOCK_STREAM

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
    
def test_good_list(client_socket):
    """Teste fim-a-fim do LIST em um caminho 'feliz'."""
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "LIST"

    message = f"{seq_num} {command}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} ARQS 16 dummyfile09-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile10-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile01-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile16-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile03-with-a-bigger-name-to-test-your-buffer-treatment.png,dummyfile12-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile11-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile04-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile06-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile14-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile07-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile02-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile08-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile13-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile05-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile15-with-a-bigger-name-to-test-your-buffer-treatment.txt"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
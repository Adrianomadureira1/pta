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

    yield clientSocket
    
def test_good_cump(client_socket):
    """Teste fim-a-fim do CUMP em um caminho 'feliz'."""
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "CUMP"
    args = "user1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} OK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))

def test_bad_cump_1(client_socket):
    """Teste do case sensitive no argumento do CUMP."""
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "CUMP"
    args = "User1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} NOK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_2(client_socket):
    """CUMP com argumento sem caracteres."""
    
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "CUMP"
    args = ""

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} NOK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_3(client_socket):
    """CUMP com argumento possuindo caracteres aleatórios."""
    
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    command = "CUMP"
    args = "dslfkspdofk"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} NOK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_4(client_socket):
    """CUMP sem número de sequência com comando e argumento corretos."""
    
    # Constrói uma mensagem

    command = "CUMP"
    args = "user1"

    message = f"{command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"0 NOK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_5(client_socket):
    """CUMP sem número de sequência e sem argumento."""
    
    # Constrói uma mensagem

    command = "CUMP"

    message = f"{command}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"0 NOK"

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_6(client_socket):
    """CUMP com número de sequência como caracteres/string."""
    # Constrói uma mensagem

    seq_num = "skdjfsdfo"
    command = "CUMP"
    args = "user1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"0 NOK"
    
    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_bad_cump_7(client_socket):
    """Comando CUMP escrito com letras minúsculas."""
    # Constrói uma mensagem

    seq_num = "skdjfsdfo"
    command = "cump"
    args = "user1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"0 NOK"
    
    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
    
def test_different_command_in_waiting_state(client_socket):
    """Comandos diferentes do CUMP em estado de espera."""
    # Constrói uma mensagem

    seq_num = "skdjfsdfo"
    command = "QDKFODFK"
    args = "user1"

    message = f"{seq_num} {command} {args}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"0 NOK"
    
    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message.decode()
    
    client_socket.send(f"0 TERM".encode("ascii"))
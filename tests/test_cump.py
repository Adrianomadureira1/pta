import random
import pytest
from socket import socket, AF_INET, SOCK_STREAM

# Todos os testes com os parâmetros configurados a seguir devem falhar!
@pytest.fixture(params=[{"message": f"100 CUMP User1", "expected": f"100 NOK"},
                        {"message": f"100 CUMP ", "expected": f"100 NOK"},
                        {"message": f"100 CUMP dlsfkpsdk", "expected": f"100 NOK"},
                        {"message": f" CUMP user1", "expected": f"0 NOK"},
                        {"message": f"CUMP user1", "expected": f"0 NOK"},
                        {"message": f"dsfdspk CUMP user1", "expected": f"0 NOK"},
                        {"message": f"100 cump user1", "expected": f"100 NOK"},
                        {"message": f"100 SDOFJHGH user1", "expected": f"100 NOK"},
                        {"message": f"100 cUmP", "expected": f"0 NOK"},
                        {"message":   f"- cUmP", "expected": f"0 NOK"},
                        {"message":    f" cUmP", "expected": f"0 NOK"},
                        {"message":     f"cUmP", "expected": f"0 NOK"},
                        {"message":     f"CUMP", "expected": f"0 NOK"}
                        ])
def cump_param(request):
    yield request.param

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

def test_bad_cump(client_socket, cump_param):
    """Teste do case sensitive no argumento do CUMP."""
    # Constrói uma mensagem

    message = cump_param["message"]

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = cump_param["expected"].encode()

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message
    
    client_socket.send(f"0 TERM".encode("ascii"))
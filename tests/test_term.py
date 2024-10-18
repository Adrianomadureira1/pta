import random, os
import pytest
import time
from socket import socket, AF_INET, SOCK_STREAM

# Todos os testes com os parâmetros configurados a seguir devem falhar!
@pytest.fixture(params=[{"message": f"100 term", "expected": f"100 NOK"},
                        {"message": f"100 tErM", "expected": f"100 NOK"},
                        {"message":   f"- tErM", "expected": f"0 NOK"},
                        {"message":    f" tErM", "expected": f"0 NOK"},
                        {"message":     f"tErM", "expected": f"0 NOK"},
                        {"message":     f"TERM", "expected": f"0 NOK"}
                        ])
def term_param(request):
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

def test_bad_term(client_socket, term_param):
    """Testes para os TERMs retornem NOK pelo servidor."""
    # Constrói uma mensagem
        
    message = term_param["message"]

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = term_param["expected"].encode("ascii")

    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(2048)
    
    assert expected_message == returned_message
    
    # Envia o TERM correto para finalizar a conexão e reiniciar o teste com outro formato de mensagem.
    client_socket.send(f"0 TERM".encode("ascii"))

def test_good_term(client_socket):
    """Teste do caminho 'feliz' para o TERM."""   
    # Constrói uma mensagem

    seq_num = random.randint(1, 10000)
    
    command = "TERM"

    message = f"{seq_num} {command}"

    # Envia mensagem

    client_socket.send(message.encode("ascii"))

    # Mensagem de retorno esperada
    
    expected_message = f"{seq_num} OK".encode("ascii")
    
    # Recebe o retorno do servidor

    returned_message, addr = client_socket.recvfrom(8182)
    
    assert expected_message == returned_message
    
    # Envia o TERM correto para finalizar a conexão.
    client_socket.send(f"0 TERM".encode("ascii"))
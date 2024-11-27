import socket
import json
import struct

# Função para escutar comandos de controle via Multicast
def listen_for_multicast():
    multicast_group = '224.1.1.1'
    server_address = ('', 10000)  # Porta 10000 para Multicast
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Permitir que vários clientes se conectem ao mesmo grupo multicast
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Adicionar o socket ao grupo multicast
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 struct.pack("4s4s", socket.inet_aton(multicast_group), socket.inet_aton('0.0.0.0')))
    multicast_socket.bind(server_address)

    print("Escutando comandos de Multicast...")

    while True:
        data, address = multicast_socket.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        print(f"Comando de cancela recebido: {message}")

        # Executar o comando na cancela (exemplo, abrir ou fechar)
        if message["type"] == "COMANDO_CANCELA":
            if message["acao"] == "Abrir":
                print(f"Abrindo a cancela: {message['cancel_id']}")
            elif message["acao"] == "Fechar":
                print(f"Fechando a cancela: {message['cancel_id']}")

# Inicia a escuta dos comandos
listen_for_multicast()

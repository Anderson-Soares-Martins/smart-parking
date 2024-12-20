import socket
import json
import time

# Função para enviar dados da câmera para o Smart Gateway via TCP
def send_camera_data(placa, timestamp):
    # Configura o socket TCP
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camera_socket.connect(('127.0.0.1', 6000))  # IP e porta do Smart Gateway

    # Mensagem com dados da câmera
    message = {
        "type": "CAMERA_DATA",
        "placa": placa,
        "timestamp": timestamp  # Pode ser uma string codificada ou um arquivo binário
    }

    # Serializa a mensagem para JSON
    message_json = json.dumps(message).encode('utf-8')

    # Envia a mensagem via TCP
    camera_socket.sendall(message_json)
    print(f"Enviado para o Smart Gateway: {message}")

    camera_socket.close()

# Envia dados da câmera periodicamente (simulando envio de imagem)
while True:
    send_camera_data("PJE2033", "2024-10-23T15:30:00")
    time.sleep(10)  # Envia a cada 10 segundos

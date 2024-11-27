import socket
import json
import time

def send_sensor_data(vaga_id, status):
    # Configura o socket UDP
    sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sensor_socket.settimeout(1)

    # Endereço do Smart Gateway (SG)
    gateway_ip = '127.0.0.1'
    gateway_port = 5005

    # Mensagem a ser enviada
    message = {
        "type": "VAGA_STATUS",
        "vaga_id": vaga_id,
        "status": status
    }

    # Serializa a mensagem para JSON
    message_json = json.dumps(message).encode('utf-8')

    # Envia a mensagem via UDP
    sensor_socket.sendto(message_json, (gateway_ip, gateway_port))
    print(f"Enviado para o SG: {message}")

    sensor_socket.close()

# Envia status das vagas periodicamente
while True:
    send_sensor_data("Vaga_1", "Livre")
    time.sleep(5)  # Espera 5 segundos antes de enviar novamente
    send_sensor_data("Vaga_1", "Ocupada")
    time.sleep(5)

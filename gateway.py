import socket
import json
import websocket
import threading

# Função para enviar dados ao servidor via WebSocket
def send_to_server(ws, message):
    try:
        ws.send(json.dumps(message))
        print(f"Enviado para o servidor: {message}")
    except Exception as e:
        print(f"Erro ao enviar dados para o servidor: {e}")

# Função para escutar o sensor via UDP
def listen_for_sensor_data(ws):
    sg_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sg_socket.bind(('0.0.0.0', 5005))  # Recebe dados do sensor na porta 5005
    print("Escutando dados do sensor via UDP...")

    while True:
        data, addr = sg_socket.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        print(f"Recebido do Sensor: {message}")

        # Envia para o servidor na nuvem via WebSocket
        if message["type"] == "VAGA_STATUS":
            vaga_data = {
                "type": "VAGA_DATA",
                "vaga_id": message["vaga_id"],
                "status": message["status"],
                "timestamp": "2024-10-23T15:30:00"
            }
            send_to_server(ws, vaga_data)

# Função para escutar os dados da câmera via TCP
def listen_for_camera_data(ws):
    # Cria o socket TCP para escutar as conexões da câmera
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camera_socket.bind(('0.0.0.0', 6000))  # Porta para a câmera
    camera_socket.listen(5)
    print("Escutando dados da câmera via TCP...")

    while True:
        client_socket, client_address = camera_socket.accept()
        print(f"Conexão com a câmera estabelecida: {client_address}")

        data = client_socket.recv(1024)
        message = json.loads(data.decode('utf-8'))
        print(f"Recebido da Câmera: {message}")

        # Envia os dados da câmera para o servidor na nuvem via WebSocket
        if message["type"] == "CAMERA_DATA":
            camera_data = {
                "type": "CAMERA_FEED",
                "camera_id": message["camera_id"],
                "image_data": message["image_data"],  # Imagem ou dados da câmera
                "timestamp": "2024-10-23T15:30:00"
            }
            send_to_server(ws, camera_data)

        client_socket.close()

# Função para escutar mensagens do servidor via WebSocket
def listen_for_server_messages(ws):
    try:
        while True:
            result = ws.recv()
            if result:
                message = json.loads(result)
                print(f"Recebido do servidor: {message}")
    except Exception as e:
        print(f"Erro ao receber dados do servidor: {e}")

# Conectar ao servidor WebSocket
def connect_to_server():
    try:
        ws = websocket.create_connection("ws://127.0.0.1:8080")
        print("Conectado ao servidor WebSocket")

        # Inicia a escuta de mensagens do servidor em uma thread separada
        server_thread = threading.Thread(target=listen_for_server_messages, args=(ws,))
        server_thread.start()

        # Inicia as threads para os sensores e a câmera
        sensor_thread = threading.Thread(target=listen_for_sensor_data, args=(ws,))
        sensor_thread.start()

        camera_thread = threading.Thread(target=listen_for_camera_data, args=(ws,))
        camera_thread.start()

        # Manter a conexão WebSocket aberta
        server_thread.join()
        sensor_thread.join()
        camera_thread.join()

    except Exception as e:
        print(f"Erro ao conectar ao servidor WebSocket: {e}")

# Inicia a conexão WebSocket com o servidor
connect_to_server()

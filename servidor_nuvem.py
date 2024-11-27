import asyncio
import websockets
import json

# Função que recebe os dados do Smart Gateway (incluindo os dados da câmera)
async def on_message(ws, path):
    try:
        async for message in ws:
            data = json.loads(message)
            print(f"Recebido do Smart Gateway: {data}")

            # Lógica para processar os dados da câmera (por exemplo, análise da imagem)
            comando = None  # Inicializa a variável comando para evitar erro

            if data["type"] == "CAMERA_FEED":
                print(f"Imagem recebida da Câmera {data['camera_id']}:\n{data['image_data']}")

                # Exemplo de comando que pode ser enviado ao Smart Gateway
                if "algum critério" in data["image_data"]:
                    comando = {
                        "type": "COMANDO_CANCELA",
                        "acao": "Fechar",
                        "cancel_id": "Cancela_1"
                    }
            # Lógica para acionar o Smart Gateway para abrir/fechar a cancela
            if data["type"] == "VAGA_DATA":
                # Exemplo de comando para a cancela
                if data["status"] == "Ocupada":
                  comando = {
                      "type": "COMANDO_CANCELA",
                      "acao": "Fechar",
                      "cancel_id": "Cancela_1"
                  }
                elif data["status"] == "Livre":
                  comando = {
                      "type": "COMANDO_CANCELA",
                      "acao": "Abrir",
                      "cancel_id": "Cancela_1"
                  }

            
            # Verifica se o comando foi atribuído antes de enviá-lo
            if comando:
                await send_command_to_sg(ws, comando)
            else:
                print("Nenhum comando a ser enviado.")

    except websockets.exceptions.ConnectionClosedOK:
        print("Conexão WebSocket fechada graciosamente.")
    except Exception as e:
        print(f"Erro ao receber dados do Smart Gateway: {e}")
    


# Função para enviar comando para o Smart Gateway (SG)
async def send_command_to_sg(ws, command):
    # Aqui você usaria o WebSocket ou outro método para enviar os comandos
    # para o Smart Gateway
    await ws.send(json.dumps(command))
    print(f"Enviado para o Smart Gateway: {command}")

# Cria o servidor WebSocket
async def main():
    # Defina a porta do servidor WebSocket
    port = 8080
    print(f"Servidor WebSocket iniciado na porta {port}")
    server = await websockets.serve(on_message, "localhost", port)
    await server.wait_closed()

# Rodando o servidor WebSocket
asyncio.run(main())

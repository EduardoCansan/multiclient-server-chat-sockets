import socket
from threading import Thread

class Server:
    Clients = []
    
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(3) #numero de conexoes (3 foi o escolhido para esse exemplo)
        print("Servidor esta aguardando conexões...")
            
    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print(f"Conexão estabelecida:" + str(address))
            
            client_name = client_socket.recv(1024).decode()
            client = {'client_name': client_name, 'client_socket': client_socket}
            
            self.broadcast_message(client_name, client_name + " entrou no chat de conversa!")
            
            Server.Clients.append(client)
            Thread(target = self.handle_new_client, args = (client,)).start()
            
    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            client_message = client_socket.recv(1024).decode()
            if client_message == client_name + ": sair" or not client_message.strip():
                self.broadcast_message(client_name, client_name + ' saiu do chat de conversa!')
                Server.Clients.remove(client)
                client_socket.close()
                break
            else:
                self.broadcast_message(client_name, client_message)
    def broadcast_message(self, sender_name, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            client_name = client['client_name']
            if client_name != sender_name:
                client_socket.send(message.encode())

if __name__ == '__main__':
    server = Server('127.0.0.1', 4567)
    server.listen()
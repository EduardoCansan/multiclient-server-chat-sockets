import os 
import socket
from threading import Thread

class Client:
    
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Digite seu nome: ")
        
        self.talk_to_server()
        
    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target = self.receive_message).start()
        self.send_message()
        
    def send_message(self):
        while True:
            client_input = input("")
            client_message = self.name + ": " + client_input
            self.socket.send(client_message.encode())
            
    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)
            print(server_message)
                
if __name__ == '__main__':
    Client('127.0.0.1', 4567)        
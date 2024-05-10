import socket
import threading

SERVER_HOST = ''
SERVER_PORT = 12345
ADDR = (SERVER_HOST,SERVER_PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

clients = []

def gestione_client(client_socket,client_address):
    name=client_socket.recv(1024).decode("utf8")
    welcome_message = "Benvenuto nella chat, "+name+"!"
    client_socket.send(bytes(welcome_message,"utf8"))
    
    broadcast(name+" è entrato nella chat", name)
    
    
    while True:
        try:
            message=client_socket.recv(1024).decode("utf8")
            
            if message == "{quit}":
                client_socket.send(bytes("{quit}", "{utf8}"))
                client_socket.close()
                rimozione_client(client_socket)
                broadcast(name + " ha lasciato la chat", name)
                break
            else:
                broadcast(message, name)
        except:
            continue    

def broadcast(message, sender_name):
    for client in clients:
        if client != server_socket:
            try:
                client.send(bytes(sender_name + ": "+message,"utf8"))
            except:
                rimozione_client(client)

def rimozione_client(client):
    if client in clients:
        clients.remove(client)

print("Server in ascolto...")

while True:
    server_socket.listen(5)
    client_socket,client_address = server_socket.accept()
    
    clients.append(client_socket)
    
    client_thread = threading.Thread(target=gestione_client(client_socket, client_address))
    client_thread.start()
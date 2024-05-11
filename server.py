import socket
import threading

SERVER_HOST = ''
SERVER_PORT = 53000
ADDR = (SERVER_HOST,SERVER_PORT)

def accept_client():
    while True:
        client, address = server_socket.accept()
        print("%s:%s si è collegato" % address)
        client.send("nickname".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        nicknames.append(nickname)
        clients.append(client)
        
        print("Il nickname del client è %s" % nickname)
        
        welcome_msg="%s si è connesso al server!\n" % nickname
        broadcast(welcome_msg)
        
        threading.Thread(target=handle_client, args=(client, nickname, )).start()

def handle_client(client, nickname):    
    while True:
        try:
            message=client.recv(1024).decode('utf-8')
            broadcast(message)
            
        except:
            remove_client(client)
            break

def broadcast(message):
    message = message.encode('utf-8')
    
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        nickname = nicknames.pop(clients.index(client))
        clients.remove(client)
        broadcast("%s ha lasciato la chat...\n" % nickname)

clients = []
nicknames = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

if __name__ == "__main__":
    server_socket.listen(5)
    print("Server in ascolto...")
       
    client_thread = threading.Thread(target=accept_client())
    client_thread.start()
    client_thread.join()
    server_socket.close()
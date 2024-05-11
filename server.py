import socket
import threading

def accept_client():
    while True:
        client,client_address = server_socket.accept()
        print("%s: %s si è collegato" %client_address)
        client.send(bytes("Digita il tuo nome: ", "utf8"))
        address[client]=client_address
        threading.Thread(target=handle_client, args=(client, )).start()

def handle_client(client_socket):   
    name=client_socket.recv(1024).decode("utf8")
    welcome_message = "Benvenuto nella chat, "+name+"!"
    client_socket.send(bytes(welcome_message,"utf8"))
    
    entry_message="%s è entrato nella chat" % name
    broadcast(bytes(entry_message, "utf8"), name)
    clients[client_socket]=name
    
    while True:
        try:
            message=client_socket.recv(1024)
            
            if message == bytes("{quit}", "utf8"):
                client_socket.send(bytes("{quit}", "utf8"))
                client_socket.close()
                remove_client(client_socket)
                broadcast(name + " ha lasciato la chat", name)
                break
            else:
                broadcast(message, name+": ")
        except:
            continue    

def broadcast(message,prefisso=""):
    for client in clients:
        try:
            client.send(bytes(prefisso,"utf8")+message)
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        clients.remove(client)

clients = {}
address = {}

SERVER_HOST = ''
SERVER_PORT = 12345
ADDR = (SERVER_HOST,SERVER_PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

if __name__ == "__main__":
    server_socket.listen(5)
    print("Server in ascolto...")
       
    client_thread = threading.Thread(target=accept_client())
    client_thread.start()
    client_thread.join()
    server_socket.close()
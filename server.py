import socket
import threading

SERVER_HOST = ''
SERVER_PORT = 53000
ADDR = (SERVER_HOST,SERVER_PORT)

def accept_client():
    while running:
        
        try:
            client, address = server_socket.accept()
            print("%s:%s si è collegato" % address)
            
            try:
                client.send("nickname".encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                
                if not nickname:
                    raise ValueError("Nickname non ricevuto")
                    
                    
                nicknames.append(nickname)
                clients.append(client)
                
                print("Il nickname del client è %s" % nickname)
                
                welcome_msg="%s si è connesso al server!\n" % nickname
                broadcast(welcome_msg)
                
                threading.Thread(target=handle_client, args=(client, nickname)).start()
                
            except Exception as e:
                print("Errore durante la ricezione del nickname: ", e)
                client.close()
                
        except Exception as e:
            if running:
                print("Errore durante l'accettazione del client: ", e)
            break

def handle_client(client, nickname):    
    while running:
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
        client.close()
        
def shutdown_server():
    global running
    running = False
    broadcast("Server chiuso. Tutte le connessioni verrano terminate")
    for client in clients:
        client.close()
    server_socket.close()
    print("Server chiuso correttamente")
    
def admin_commands():
    while True:
        command = input("")
        if command.lower() == "quit" or command.lower() == "shutdown":
            print("Chiusura del server...")
            shutdown_server()
            break

clients = []
nicknames = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

running = True

if __name__ == "__main__":
    server_socket.listen(5)
    print("Server in ascolto...")
       
    client_thread = threading.Thread(target=accept_client)
    client_thread.start()
    
    admin_thread = threading.Thread(target=admin_commands)
    admin_thread.start()    
    
    client_thread.join()
    admin_thread.join()
        
        
        
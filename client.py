import socket
import threading
import tkinter as tk

SERVER_HOST = input("Inserisci il server host: ")
SERVER_PORT = int(input("Inserisci il server port: ") or 12345)
ADDR = (SERVER_HOST, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def ricevimento():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            message_list.insert(tk.END, message)
            message_list.see(tk.END)
        except OSError:
            break       
        
def invio():
    while True:
        message = input()
        client_socket.send(bytes(message,"utf8"))

window = tk.Tk()
window.title("Chat Client")

message_frame=tk.Frame(window)

my_message = tk.StringVar()
my_message.set("Scrivi i tuoi messaggi")
scrollbar = tk.Scrollbar(message_frame)

message_list = tk.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_frame.pack()

entry_field = tk.Entry(window,textvariable=my_message)
entry_field.bind("<Return>", invio)
entry_field.pack()

send_button = tk.Button(window, text="Invia", command=invio)
send_button.pack()

receive_thread = threading.Thread(target=ricevimento)
receive_thread.start()

window.mainloop()
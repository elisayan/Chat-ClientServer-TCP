import socket
import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog

class Client:
    
    def __init__(self):    
        self.server_host = None
        self.server_post = None
        self.sock = None
        
    def askHost(self):
        while True:
            server_host = input("Inserisci il server host: ")
            
            try:
                socket.gethostbyname(server_host)
                self.server_host = server_host;
                break
            except socket.gaierror:
                print ("Host non valido, riprova")
                
    def connectionServer(self):
        while True:
            try:            
                server_port = int(input("Inserisci il server port: ") or 53000)
                ADDR = (self.server_host,server_port)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(ADDR)
                print("Connessione riuscita!")
                break
            except socket.error as e:
                print("Errore di connessione: ", e)
                print("Riprova...")
    
    def gui_loop(self):
        self.win=tk.Tk()
        self.win.title("Chat Room")
        self.win.configure(bg="lightgray")
        
        self.chat_label=tk.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tk.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label=tk.Label(self.win, text="Messaggio: ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)
        
        self.input_area = tk.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
        
        self.send_button = tk.Button(self.win, text="Invia", command = self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        
        self.gui_done=True
        
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()
        
    def write(self):
        message_text=self.input_area.get('1.0','end').strip()
        message = self.nickname+": "+ message_text + "\n"
        if self.sock:
            try:
                self.sock.send(message.encode('utf-8'))
            except OSError as e:
                print("Errore durante l'invio del messaggio: ", e)
        self.input_area.delete('1.0', 'end')
        
    def stop(self):
        self.running=False
        self.win.destroy()
        if self.sock:
            self.sock.close()
        exit(0)
    
    def receive(self):
        while self.running:            
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'nickname':
                    self.sock.send(self.nickname.encode('utf-8'))
                elif message == "Server chiuso. Tutte le connessioni verrano terminate":
                    print(message)
                    self.sock.close()
                    self.running = False
                    self.stop()   
                    break
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except OSError:
                break
            except Exception as e:
                print("Errore: ", e)
                if self.sock:
                    self.sock.close()
                break
            
def main():
    client = Client()
    client.askHost()
    client.connectionServer()
    msg = tk.Tk()
    msg.withdraw()
    
    client.nickname = simpledialog.askstring("Nickname", "Inserisci il tuo nickname", parent=msg)
    
    client.gui_done = False
    client.running = True

    gui_thread = threading.Thread(target=client.gui_loop)
    receive_thread = threading.Thread(target=client.receive)
    
    gui_thread.start()
    receive_thread.start()

if __name__ == "__main__":
    main()
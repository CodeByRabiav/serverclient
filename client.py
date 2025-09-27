
import socket
import tkinter as tk
from tkinter import filedialog

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def send_message():
    msg = entry.get()
    if msg:
        client_socket.send("MSG".ljust(16).encode())  # başlık
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()
        chat_box.insert(tk.END, "Sunucu: " + data + "\n")
        entry.delete(0, tk.END)

def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        filename = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        client_socket.send("FILE".ljust(16).encode())
        client_socket.send(f"{filename}|{len(file_data)}".ljust(256).encode())
        client_socket.sendall(file_data)
        data = client_socket.recv(1024).decode()
        chat_box.insert(tk.END, "Sunucu: " + data + "\n")


root = tk.Tk()
root.title("Client Arayüzü")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=5, pady=5)

send_button = tk.Button(root, text="Mesaj Gönder", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(root, text="Dosya Gönder", command=send_file)
file_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
client_socket.close()

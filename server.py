import socket
import threading
import os
import tkinter as tk
from PIL import Image, ImageTk

HOST = "127.0.0.1"  # server IP
PORT = 12345         # server port

root = tk.Tk()
root.title("Server Interface")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack(padx=10, pady=10)

img_label = tk.Label(root)
img_label.pack()

def handle_client(conn, addr):
    chat_box.insert(tk.END, f"{addr} connected.\n")
    try:
        while True:
            header = conn.recv(16)
            if not header:
                break
            header = header.decode().strip()

            if header == "MSG":
                data = conn.recv(1024).decode()
                chat_box.insert(tk.END, f"{addr} -> Message: {data}\n")
                conn.send(f"Message received: {data}".encode())

            elif header == "FILE":
                meta = conn.recv(256).decode().strip()
                filename, filesize = meta.split("|")
                filesize = int(filesize)
                file_data = b""
                while len(file_data) < filesize:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    file_data += packet
                save_path = f"server_{filename}"
                with open(save_path, "wb") as f:
                    f.write(file_data)
                chat_box.insert(tk.END, f"{addr} -> File received: {filename}\n")
                conn.send(f"{filename} received".encode())

                if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                    try:
                        img = Image.open(save_path)
                        img.thumbnail((400, 400))
                        tk_img = ImageTk.PhotoImage(img)
                        img_label.config(image=tk_img)
                        img_label.image = tk_img
                    except Exception as e:
                        chat_box.insert(tk.END, f"Image error: {e}\n")

                    os.startfile(save_path)

    finally:
        conn.close()
        chat_box.insert(tk.END, f"{addr} disconnected.\n")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
chat_box.insert(tk.END, "Server running...\n")

def accept_clients():
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

threading.Thread(target=accept_clients, daemon=True).start()
root.mainloop()
server.close()

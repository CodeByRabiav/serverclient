import socket
import threading
import os
import platform
import tkinter as tk
from PIL import Image, ImageTk

HOST = "127.0.0.1" #sunucunun dinleyeceği port
PORT = 12345 #sunucunun bağlanacağı port client burada bağlanacak


root = tk.Tk() #tkinder penceresini aktif ediyoruz
root.title("Sunucu Arayüzü") #pencere başlıı

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack(padx=10, pady=10) #pencere eklendi 


img_label = tk.Label(root) #resimler burada gösterilecek
img_label.pack() #sonradan eklenen resimler için


def istemci_isle(conn, addr):
    chat_box.insert(tk.END, f"{addr} bağlandi.\n")
    try:
        while True:
            header = conn.recv(16)
            if not header:
                break
            header = header.decode().strip()

            if header == "MSG":
                data = conn.recv(1024).decode()
                chat_box.insert(tk.END, f"{addr} -> Mesaj: {data}\n")
                conn.send(f"Mesaj alindi: {data}".encode())

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
                chat_box.insert(tk.END, f"{addr} -> Dosya alindi: {filename}\n")
                conn.send(f"{filename} alindi".encode())

                # Eğer resim ise Tkinter ile göster
                if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                    try:
                        img = Image.open(save_path)
                        img.thumbnail((400, 400))  # pencereye sığdır
                        tk_img = ImageTk.PhotoImage(img)
                        img_label.config(image=tk_img)
                        img_label.image = tk_img  # referans kaybolmasın
                    except Exception as e:
                        chat_box.insert(tk.END, f"Resim yok: {e}\n")
               
                
                    os.startfile(save_path)
                
    finally:
        conn.close()
        chat_box.insert(tk.END, f"{addr} bağlantisi kapand..\n")

# Sunucu başlat
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
chat_box.insert(tk.END, "Sunucu çalisiyor...\n")

def istemcileri_kabulet():
    while True:
        conn, addr = server.accept()
        threading.Thread(target=istemci_isle, args=(conn, addr), daemon=True).start()

threading.Thread(target=istemcileri_kabulet, daemon=True).start()
root.mainloop()
server.close()

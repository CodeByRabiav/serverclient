import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import os
import io
import queue


HOST = "127.0.0.1"
PORT = 12345

def caesar_decrypt(text, key):
    result = ""
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            result += chr((ord(ch) - shift - key) % 26 + shift)
        else:
            result += ch
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    k = 0
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            result += chr((ord(ch) - shift - (ord(key[k % len(key)]) - 97)) % 26 + shift)
            k += 1
        else:
            result += ch
    return result

def substitution_decrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    rev_key = "".join(sorted(alphabet, key=lambda x: key.index(x)))
    table = str.maketrans(key.lower() + key.upper(), alphabet + alphabet.upper())
    return text.translate(table)

def affine_decrypt(text, a, b):
    result = ""
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            a_inv = pow(a, -1, 26)
            result += chr((a_inv * ((ord(ch) - shift) - b)) % 26 + shift)
        else:
            result += ch
    return result

def handle_client(conn, addr):
    chat.insert(tk.END, f"{addr} bağlandi.\n")
    while True:
        data = conn.recv(4096)
        if not data:
            break
        if data.startswith(b"FILE"):
            chat.insert(tk.END, "Dosya alindi.\n")
        else:
            msg = data.decode()
            chat.insert(tk.END, f"Gelen şifreli metin: {msg}\n")

    conn.close()
    chat.insert(tk.END, f"{addr} ayrildi.\n")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    chat.insert(tk.END, "Sunucu başlatildi...\n")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
[{
	"resource": "/c:/Users/rabia/OneDrive/Masaüstü/serverclient2/client_gui.py",
	"owner": "pylance",
	"code": {
		"value": "reportUndefinedVariable",
		"target": {
			"$mid": 1,
			"path": "/microsoft/pylance-release/blob/main/docs/diagnostics/reportUndefinedVariable.md",
			"scheme": "https",
			"authority": "github.com"
		}
	},
	"severity": 4,
	"message": "\"msg_queue\" is not defined",
	"source": "Pylance",
	"startLineNumber": 121,
	"startColumn": 25,
	"endLineNumber": 121,
	"endColumn": 34,
	"origin": "extHost1"
}]
root = tk.Tk()
root.title("Server - Şifre Çözme")

chat = tk.Text(root, height=20, width=60)
chat.pack(padx=10, pady=10)

tk.Button(root, text="Sunucuyu Başlat", command=lambda: threading.Thread(target=start_server, daemon=True).start()).pack(pady=5)

root.mainloop()

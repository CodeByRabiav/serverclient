import socket
import tkinter as tk
from tkinter import ttk, filedialog

HOST = "127.0.0.1"
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def caesar_encrypt(text, key):
    result = ""
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            result += chr((ord(ch) - shift + key) % 26 + shift)
        else:
            result += ch
    return result

def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    k = 0
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            result += chr((ord(ch) - shift + (ord(key[k % len(key)]) - 97)) % 26 + shift)
            k += 1
        else:
            result += ch
    return result

def substitution_encrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    table = str.maketrans(alphabet + alphabet.upper(), key.lower() + key.upper())
    return text.translate(table)

def affine_encrypt(text, a, b):
    result = ""
    for ch in text:
        if ch.isalpha():
            shift = 65 if ch.isupper() else 97
            result += chr(((a * (ord(ch) - shift) + b) % 26) + shift)
        else:
            result += ch
    return result

# --- İşlevler ---
def encrypt_text():
    text = txt_input.get("1.0", tk.END).strip()
    key = ent_key.get()
    method = combo_method.get()

    if not text or not key:
        txt_output.insert(tk.END, " Metin veya anahtar eksik!\n")
        return

    try:
        if method == "Caesar":
            result = caesar_encrypt(text, int(key))
        elif method == "Vigenere":
            result = vigenere_encrypt(text, key)
        elif method == "Substitution":
            result = substitution_encrypt(text, key)
        elif method == "Affine":
            a, b = map(int, key.split(","))
            result = affine_encrypt(text, a, b)
        else:
            result = text

        txt_output.insert(tk.END, f" Şifrelenmiş: {result}\n")
        client.send(result.encode())

    except Exception as e:
        txt_output.insert(tk.END, f"Hata: {e}\n")

def send_file():
    path = filedialog.askopenfilename()
    if not path:
        return
    with open(path, "rb") as f:
        data = f.read()
    client.send(b"FILE" + data)
    txt_output.insert(tk.END, " Dosya gönderildi.\n")



root = tk.Tk()
root.title(" Client - Şifreleme Uygulaması")
root.geometry("520x600")
root.config(bg="#f0f0f0")


frm_main = tk.LabelFrame(root, text="Şifreleme İşlemi", bg="#f0f0f0", padx=10, pady=10)
frm_main.pack(padx=10, pady=10, fill="both")

tk.Label(frm_main, text="Şifreleme Yöntemi:", bg="#f0f0f0", font=("Segoe UI", 10)).pack(anchor="w")
combo_method = ttk.Combobox(frm_main, values=["Caesar", "Vigenere", "Substitution", "Affine"], state="readonly", width=25)
combo_method.current(0)
combo_method.pack(pady=5)

tk.Label(frm_main, text="Anahtar:", bg="#f0f0f0", font=("Segoe UI", 10)).pack(anchor="w")
ent_key = ttk.Entry(frm_main, width=30)
ent_key.pack(pady=5)

tk.Label(frm_main, text="Metin Girişi:", bg="#f0f0f0", font=("Segoe UI", 10)).pack(anchor="w")
txt_input = tk.Text(frm_main, height=5, width=50)
txt_input.pack(pady=5)

btn_encrypt = ttk.Button(frm_main, text="Şifrele ve Gönder", command=encrypt_text)
btn_encrypt.pack(pady=5)

btn_file = ttk.Button(frm_main, text="Dosya Gönder", command=send_file)
btn_file.pack(pady=5)


frm_result = tk.LabelFrame(root, text="Sunucudan Gelen Yanıtlar", bg="#f0f0f0", padx=10, pady=10)
frm_result.pack(padx=10, pady=10, fill="both", expand=True)

txt_output = tk.Text(frm_result, height=10, width=60)
txt_output.pack()

root.mainloop()
client.close()

import socket
import pyperclip

HOST = "192.168.1.50"   # IP of the HOST PC
PORT = 5000

def send_clipboard():
    text = pyperclip.paste()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(text.encode("utf-8"))
    s.close()

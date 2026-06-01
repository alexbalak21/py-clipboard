import socket
import pyperclip

HOST = "192.168.1.44"   # IP of the HOST PC
PORT = 5000

def send_clipboard():
    text = pyperclip.paste()

    if not text.strip():
        return  # don't send empty clipboard

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(text.encode("utf-8"))
        s.close()
        print("Clipboard sent.")
    except Exception as e:
        print(f"Error sending clipboard: {e}")

import socket
import pyperclip

HOST = "192.168.1.44"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Clipboard Host running...")

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    chunks = []
    while True:
        data = conn.recv(4096)
        if not data:
            break
        chunks.append(data)

    text = b"".join(chunks).decode("utf-8", errors="ignore")

    if text:
        pyperclip.copy(text)
        print(f"Received clipboard: {text}")

    conn.close()

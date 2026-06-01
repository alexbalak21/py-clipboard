import socket
import pyperclip

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Clipboard Host running...")

while True:
    conn, addr = server.accept()
    data = conn.recv(4096).decode("utf-8")
    if data:
        pyperclip.copy(data)
        print(f"Received clipboard: {data}")
    conn.close()

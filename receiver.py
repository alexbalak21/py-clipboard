import socket
import threading
import time
import pyperclip
# WORKS on TEXT
HOST = "0.0.0.0"
PORT = 5000
BROADCAST_PORT = 6000

# ---------------------------
# UDP BROADCAST THREAD
# ---------------------------
def broadcast_presence():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        msg = f"RECEIVER;PORT={PORT}".encode()
        sock.sendto(msg, ("255.255.255.255", BROADCAST_PORT))
        time.sleep(2)


# ---------------------------
# TCP CLIPBOARD RECEIVER
# ---------------------------
def start_receiver():
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


# ---------------------------
# MAIN
# ---------------------------
threading.Thread(target=broadcast_presence, daemon=True).start()
start_receiver()

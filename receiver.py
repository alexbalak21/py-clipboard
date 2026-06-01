import socket
import threading
import time
import pyperclip
import tempfile
import os

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

        # Read header until blank line
        header = b""
        while b"\n\n" not in header:
            header += conn.recv(1)

        header_text = header.decode()
        lines = header_text.strip().split("\n")
        data_type = lines[0].split(":")[1]
        size = int(lines[1].split(":")[1])

        # Read payload
        data = b""
        while len(data) < size:
            data += conn.recv(4096)

        if data_type == "TEXT":
            text = data.decode("utf-8", errors="ignore")
            pyperclip.copy(text)
            print(f"Received TEXT: {text}")

        elif data_type == "IMAGE":
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp.write(data)
            temp.close()
            print(f"Received IMAGE saved to: {temp.name}")
            os.startfile(temp.name)  # auto-open image

        conn.close()


# ---------------------------
# MAIN
# ---------------------------
threading.Thread(target=broadcast_presence, daemon=True).start()
start_receiver()

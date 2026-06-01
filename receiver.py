import socket
import threading
import time
import pyperclip
import tempfile
import os
import subprocess

HOST = "0.0.0.0"
PORT = 5000
BROADCAST_PORT = 6000

# WORKING WITH TEXT & IMAGES, PUTTING THE IMAGE DIRECTLY IN THE CLIPBOARD OF THE RECEIVER

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
# PUT IMAGE INTO WINDOWS CLIPBOARD
# ---------------------------
def set_clipboard_image(image_path):
    subprocess.run([
        "powershell", "-command",
        f"Add-Type -AssemblyName System.Windows.Forms;"
        f"$img=[System.Drawing.Image]::FromFile('{image_path}');"
        f"[System.Windows.Forms.Clipboard]::SetImage($img)"
    ], check=True)


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

        # Read header
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

        # TEXT
        if data_type == "TEXT":
            text = data.decode("utf-8", errors="ignore")
            pyperclip.copy(text)
            print(f"Received TEXT: {text}")

        # IMAGE
        elif data_type == "IMAGE":
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp.write(data)
            temp.close()

            print(f"Received IMAGE → putting into clipboard")

            # Put image directly into clipboard
            set_clipboard_image(temp.name)

            # Optional: delete file
            os.remove(temp.name)

        conn.close()


# ---------------------------
# MAIN
# ---------------------------
threading.Thread(target=broadcast_presence, daemon=True).start()
start_receiver()

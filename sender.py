import socket
import pyperclip
import time
import subprocess
import tempfile
import os
import hashlib

BROADCAST_PORT = 6000
receiver_ip = None
receiver_port = None

last_text = ""
last_image_hash = None


# ---------------------------
# DISCOVER RECEIVER
# ---------------------------
def discover_receiver():
    global receiver_ip, receiver_port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", BROADCAST_PORT))

    print("Searching for receiver on LAN...")

    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        if msg.startswith("RECEIVER"):
            receiver_ip = addr[0]
            receiver_port = int(msg.split("PORT=")[1])
            print(f"Receiver found at {receiver_ip}:{receiver_port}")
            break


# ---------------------------
# GET IMAGE FROM CLIPBOARD
# ---------------------------
def get_clipboard_image():
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp.close()

    try:
        subprocess.run([
            "powershell", "-command",
            f"Add-Type -AssemblyName System.Windows.Forms;"
            f"$img=[System.Windows.Forms.Clipboard]::GetImage();"
            f"if ($img) {{$img.Save('{temp.name}')}}"
        ], check=True)

        if os.path.getsize(temp.name) > 0:
            return temp.name
        else:
            os.remove(temp.name)
            return None

    except:
        return None


# ---------------------------
# HASH FILE
# ---------------------------
def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------------------
# SEND CLIPBOARD
# ---------------------------
def send_clipboard():
    img_path = get_clipboard_image()

    if img_path:
        with open(img_path, "rb") as f:
            data = f.read()
        os.remove(img_path)

        header = f"TYPE:IMAGE\nSIZE:{len(data)}\n\n".encode()
        payload = header + data

    else:
        text = pyperclip.paste().encode("utf-8")
        header = f"TYPE:TEXT\nSIZE:{len(text)}\n\n".encode()
        payload = header + text

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((receiver_ip, receiver_port))
        s.sendall(payload)
        s.close()
        print("Clipboard sent.")
    except Exception as e:
        print(f"Error sending clipboard: {e}")


# ---------------------------
# MAIN LOOP
# ---------------------------
discover_receiver()

print("Clipboard watcher running...")

while True:
    # Check for image
    img_path = get_clipboard_image()
    if img_path:
        new_hash = hash_file(img_path)
        os.remove(img_path)

        if new_hash != last_image_hash:
            last_image_hash = new_hash
            print("Detected new IMAGE clipboard, sending...")
            send_clipboard()

        time.sleep(0.3)
        continue

    # Check for text
    current_text = pyperclip.paste()
    if current_text != last_text:
        last_text = current_text
        last_image_hash = None
        print("Detected new TEXT clipboard, sending...")
        send_clipboard()

    time.sleep(0.3)

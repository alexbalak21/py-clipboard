import socket
import pyperclip
import time
# WORKS on TEXT
BROADCAST_PORT = 6000
receiver_ip = None
receiver_port = None


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
# SEND CLIPBOARD
# ---------------------------
def send_clipboard():
    text = pyperclip.paste()

    if not text.strip():
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((receiver_ip, receiver_port))
        s.sendall(text.encode("utf-8"))
        s.close()
        print("Clipboard sent.")
    except Exception as e:
        print(f"Error sending clipboard: {e}")


# ---------------------------
# MAIN
# ---------------------------
discover_receiver()

last_text = pyperclip.paste()
print("Clipboard watcher running...")

while True:
    current = pyperclip.paste()
    if current != last_text:
        last_text = current
        print("Detected new clipboard, sending...")
        send_clipboard()
    time.sleep(0.2)

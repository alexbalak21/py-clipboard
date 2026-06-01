import socket

BROADCAST_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", BROADCAST_PORT))

print("Listening for receiver...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    if msg.startswith("RECEIVER"):
        port = int(msg.split("PORT=")[1])
        receiver_ip = addr[0]
        print(f"Receiver found at {receiver_ip}:{port}")
        break

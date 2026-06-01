import socket
import time

PORT = 5000
BROADCAST_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    message = f"RECEIVER;PORT={PORT}".encode()
    sock.sendto(message, ("255.255.255.255", BROADCAST_PORT))
    time.sleep(2)

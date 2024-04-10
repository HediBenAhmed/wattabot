import socket
from services.CameraService import PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", PORT))
    while True:
        x = input("x,y")
        s.sendall(x.encode("utf-8"))
        data = s.recv(1024)
        print(f"Received {data!r}")

import socket
import struct


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)


class SocketService:
    def __init__(self, port):
        self.port = port

    def runAction(self, action: str):
        pass

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Port to listen on (non-privileged ports are > 1023)
            s.bind((HOST, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    action = conn.recv(1024).decode("utf-8")
                    if not action:
                        break
                    data = self.runAction(action)

                    if data == None:
                        data = action.encode()

                    messageSize = struct.pack("<L", len(data))
                    conn.sendall(messageSize + data)

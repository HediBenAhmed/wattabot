import socket
import struct


class SocketClientService:
    def __init__(self, host, port):
        self.port = port
        self.host = host

    def connect(self):
        socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketClient.connect((self.host, self.port))

        self.socketClient = socketClient

    def sendRequest(self, request: str, waitResponse=True):
        self.socketClient.sendall(request.encode("utf-8"))

        if waitResponse:

            msgSize = self.socketClient.recv(struct.calcsize("<L"))
            msgSize = struct.unpack("<L", msgSize)[0]

            # Retrieve all data based on message size
            data = self.socketClient.recv(msgSize)
            return data

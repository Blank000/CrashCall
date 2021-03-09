import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server
BROADCAST_PORT = 24321
bufferSize = 1024
encoding = "utf-8"


def connectingTCPServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(input().encode())
            data = s.recv(1024)
            print('Received', repr(data))


def connectingUDPServer():
    serverAddressPort = (HOST, PORT)
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(str.encode(input()), serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0].decode(encoding))
    print(msg)



connectingUDPServer()

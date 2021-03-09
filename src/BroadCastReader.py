import socket
import struct

HOST = '127.0.0.1'  # The server's hostname or IP address
BROADCAST_PORT = 24321
bufferSize = 1024
encoding = "utf-8"


def receivingDataFromBroadcatServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # For macbook comment the above line and use this line

    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client.bind((HOST, BROADCAST_PORT))
    while True:
        data, addr = client.recvfrom(1024)
        print("received message: %s" % data.decode(encoding))


def multi_casting():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    IS_ALL_GROUPS = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # For macbook comment the above line and use this line
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        # For Python 3, change next line to "print(sock.recv(10240))"
        print(sock.recv(1024).decode(encoding))

multi_casting()

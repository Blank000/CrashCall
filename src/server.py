''' Socket programming in python, for TCP we can create a socket object using socket.socket() and specify the socket type as socket.SOCK_STREAM.
 For UDP the socket type is defined as socket.SOCK_DGRAM
 We can use the command :- lsof -i -n  to see the active TCP connections
 '''
import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
encoding = "utf-8"
bufferSize = 1024
BROADCAST_PORT = 24321


class ListenerThread(threading.Thread):
    """The Listener Thread grabs incoming packets, parses them and forwards them to the right listeners"""

    def __init__(self, socket, handler):
        super(ListenerThread, self).__init__(
            name='ListenerThread'
        )

        # Exit on script exit
        self.daemon = True

        # Store instance data
        self._socket = socket
        self._handler = handler

    def run(self):
        while True:
            data, addr = self._socket.recvfrom(1500)
            self._handler(addr, protocol.parse_packet(data))


def createTCPConnection():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)


def createUDPConnection():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((HOST, PORT))
    print("UDP server up and listening")
    # Listen for incoming datagrams
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        mssg = bytesAddressPair[0].decode(encoding)
        name, lat, lon = mssg.split(",")
        address = bytesAddressPair[1]
        mssgFromClient = "Message from Client:{}".format(mssg)
        clientIP = "Client IP Address:{}".format(address)
        msgFromServer = f"Hello {name}, Sending emegency services to your location ({lat},{lon})"
        print(f"Client with IP {clientIP} has sent mssg :- {mssgFromClient}")
        broadCastMsg = f"Client {name} has met an accident at location ({lat}, {lon})"
        # Sending a reply to client
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
        broadCastMessageWithUDP(broadCastMsg)


'''
def broadCastMessageWithUDP(broadCastMsg):
    print(f"Broadcasting data from the port {BROADCAST_PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)

    server.sendto(broadCastMsg.encode(), ('<broadcast>', BROADCAST_PORT))
    print("message Broadcasted!")
'''


def broadCastMessageWithUDP(broadCastMsg):
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    # For Python 3, change next line to 'sock.sendto(b"robot", ...' to avoid the
    # "bytes-like object is required" msg (https://stackoverflow.com/a/42612820)
    sock.sendto(broadCastMsg.encode(), (MCAST_GRP, MCAST_PORT))
    print("Message BroadCasted")


createUDPConnection()

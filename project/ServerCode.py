# Maria Hajj
# Server code using TCP

from Heartbeat import HeartBeat
from socket import AF_INET, SOCK_STREAM
import socket
import os
import struct
import hashlib


TCP_IP = 'localhost'
TCP_PORT = 15010
BUFFER_SIZE = 1024
codePath = '/Users/MariaHajj/Desktop/FALL 2020/CMPS 284/Project/'
file = codePath+'testfile.txt'


# set up the TCP server
addr = (TCP_IP, TCP_PORT)
sock = socket.socket(AF_INET, SOCK_STREAM)
sock.bind(('', TCP_PORT))
sock.listen(3)

client, addr = sock.accept()
print('Connection from:', addr)


# goes over the file list array to cut the file in chunks
def handle(client, addr):
    print('File size:', os.path.getsize(file))
    file_size = struct.pack('!I', os.path.getsize(file))
    print('Len of file size struct:', len(file_size))
    client.send(file_size)
    with open(file, 'rb') as fopen:
        while True:
            chunk = fopen.read(BUFFER_SIZE)
            if not chunk:
                break
            client.send(chunk)
        fopen.seek(0)
        hash = hashlib.sha512()
        while True:
            chunk = fopen.read(BUFFER_SIZE)
            if not chunk:
                break
            hash.update(chunk)
        client.send(hash.digest())
    client.close()


handle(client, addr)

# Runs the hearbeat UDP part
HeartBeat()

# checks if the request timed out
if(HeartBeat.response is True):
    print('Request Timed out. Peer dropped.')

sock.close()

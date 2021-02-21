# Maria Hajj
# Client code using TCP

import socket
import struct
import hashlib
from socket import AF_INET, SOCK_STREAM

# some variables
TCP_IP = 'localhost'
TCP_PORT = 15010
BUFFER_SIZE = 1024
chunks = []
received = 0

# set up the socket
addr = (TCP_IP, TCP_PORT)
sock = socket.socket(AF_INET, SOCK_STREAM)
sock.connect(addr)
print('Connected to', addr)

# all while loops to make sure all chunks are received
while received < 4:
    data = sock.recv(4 - received)
    received += len(data)
    chunks.append(data)
print('Received len of file size struct', len(b''.join(chunks)))
file_size = struct.unpack('!I', b''.join(chunks))[0]
print('Filesize:', file_size)


while received < file_size:
    data = sock.recv(min(file_size - received, BUFFER_SIZE))
    received += len(data)
    chunks.append(data)
file = b''.join(chunks)
print('Received file')
print('Expected size:', file_size)
print('Received size:', len(file))


while received < 64:
    data = sock.recv(64 - received)
    received += len(data)
    chunks.append(data)
sha512 = b''.join(chunks)

# checks if the hashing is correct
hash_correct = hashlib.sha512(file).digest()
if (hash_correct == sha512):
    print('Hash is correct')
else:
    print('Hash is not correct')

sock.close()

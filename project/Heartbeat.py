import socket
import time
from socket import AF_INET, SOCK_DGRAM

# the server hostname and port
TCP_IP = 'localhost'
TCP_PORT = 15010
timeout = 5  # in second
# boolean variable to keep track if there was a timeout
#  True is timeout False if not
response = False


class HeartBeat():

    # Create UDP client socket
    # Note the use of SOCK_DGRAM for UDP datagram packet
    clientsocket = socket.socket(AF_INET, SOCK_DGRAM)
    # Set socket timeout as 1 second
    clientsocket.settimeout(timeout)
    # Sequence number of the ping message
    ptime = 0

    # Ping for 10 times
    while ptime < 10:
        ptime += 1
        # Format the message to be sent
        data = "Ping " + str(ptime) + " " + time.asctime()

        try:
            # Sent time
            RTTb = time.time()
            # Send the UDP packet with the ping message
            clientsocket.sendto(data.encode(), (TCP_IP, TCP_PORT))
            # Receive the server response
            message, address = clientsocket.recvfrom(1024)
            # Received time
            RTTa = time.time()
            # Display the server response as an output
            print("Reply from " + address[0] + ": " + message.decode())
            # Round trip time is the difference between sent and received time
            print("RTT: " + str(RTTa - RTTb))

        except Exception:
            # Server does not response
            # Assume the packet is lost
            response = True
            continue

    # Close the client socket
    clientsocket.close()

"""
Where solution code to project should be written.  No other files should
be modified.
"""

import socket
import io
import time
import typing
import struct
import util
import util.logging
import threading
from threading import Timer

# Timer
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

# Resends the global packet using the timer thread
def resend():
    sock_global.send(packet_global)
    mess, seq = getInfo(packet_global)
    print("Resending Packet:", seq)

# Sets up the packet
def pktBuilder(seq, p):
    pkt = p.decode("utf-8")
    pkt += ";" + str(seq)
    return bytes(str.encode(pkt))

# Retreives the data and sequence number in a packet
def getInfo(d):
    data = d.decode("utf-8")
    info = data.split(";")
    mess = info[0]
    seq = info[1]
    return mess, seq

def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Initializations
    sock.setblocking(0)
    chunk_size = util.MAX_PACKET - 8    # Size of packet in this case will never be more than 5 digits long plus one bit for the delimiter
    offsets = range(0, len(data), util.MAX_PACKET - 8)
    ackedPkts = []
    pkts = []
    seq_num = 0
    pkt_number = 0
    isAcknowledged = None    # boolean to see if the current packet has been isAcknowledged
    timer = RepeatTimer(0.2, resend)
    global packet_global
    global sock_global
    sock_global = sock

    # Save all packets in a list
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        pkt = pktBuilder(seq_num, chunk)
        pkts.append(pkt)
        seq_num += len(chunk)

    # Start timer
    packet_global = pkts[pkt_number]
    timer.start()
    while True:
        # Receive acks
        try:
            ackData = sock.recv(util.MAX_PACKET)
            print("Ack received!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ack = int.from_bytes(ackData, "big")
            if ack not in ackedPkts:
                print("RECEIVED NEW ACK:", ack)
                ackedPkts.append(ack)
                pkt_number += 1
                packet_global = pkts[pkt_number]
        except:
            pass

        # Terminate Program
        if pkt_number >= len(pkts):
            print("ALL PACKETS HAVE BEEN SENT")
            timer.cancel()
            break



def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    pktsRecv = []
    acksSent = []
    pause = .1
    num_bytes = 0
    while True:
        # Receive packets
        data = sock.recv(util.MAX_PACKET)
        if not data:
            break
        message, seq_num = getInfo(data)
        print("***********************************************************")
        print("Received sequence number:" , seq_num)
        # Create and send acks
        ack_num = int(seq_num) + len(message)
        ack = ack_num.to_bytes(3, "big")
        print("Sending ack:", ack_num)
        if ack_num not in acksSent:
            dest.write(bytes(str.encode(message)))
            dest.flush()
            acksSent.append(ack_num)
            pktsRecv.append(bytes(str.encode(message)))
        sock.send(ack)
        num_bytes += len(message)
    return num_bytes

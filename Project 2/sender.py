# Written by S. Mevawala, modified by D. Gitzel

# ECE303 Communication Networks
# Project 2: Selective Repeat simulator
# Jon Lu & David Yang 05/02/2021

import logging
import socket
import sys
import channelsimulator
import utils

import array
import hashlib

class Sender(object):
    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=1, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

class RDTSender(Sender):
    senderRDTBit = 0

    timeout = 0.1
    packetStart = 0
    packetEnd = MaxSegSize = 991

    currentSegment = []

    def __init__(self):
        super(RDTSender, self).__init__()

    def send(self, payload):
        while self.packetStart < len(payload):
            try:
                if self.packetEnd > len(payload):
                    data = payload[self.packetStart:len(payload)]

                else:
                    data = payload[self.packetStart:self.packetEnd]

                self.currentSegment = str(self.senderRDTBit) + str(checksumGet(data)) + data

                self.simulator.u_send(self.currentSegment)
                self.simulator.sndr_socket.settimeout(self.timeout)

                while 1:
                    returnSegment = self.simulator.u_receive()

                    returnRDTBit = returnSegment[0:1]
                    returnChecksum = returnSegment[1:33]

                    if (str(self.senderRDTBit) == returnRDTBit) and (str(checksumGet(data)) == returnChecksum):
                        self.simulator.sndr_socket.settimeout(None)
                        self.packetStart += self.MaxSegSize
                        self.packetEnd += self.MaxSegSize
                        self.senderRDTBit = 1 - self.senderRDTBit
                        break

            except socket.timeout:
                self.simulator.u_send(self.currentSegment)
        print("DONE")
        sys.exit()

def checksumGet(data):
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    sender = RDTSender()
    sender.send(sys.stdin.read())

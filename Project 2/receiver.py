# Written by S. Mevawala, modified by D. Gitzel

# ECE303 Communication Networks
# Project 2: Selective Repeat simulator
# Jon Lu & David Yang 05/02/2021

import logging
import channelsimulator
import utils
import sys
import socket

import array
import hashlib

class Receiver(object):
    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=5, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

class RDTReceiver(Receiver):
    expectedRDTBit = 0

    def __init__(self):
        super(RDTReceiver, self).__init__()

    def receive(self):
        try:
            while 1:
                receivedSegment = self.simulator.u_receive()

                receivedRDTBit = receivedSegment[0:1]
                checksum = receivedSegment[1:33]
                data = receivedSegment[33:]

                if (str(self.expectedRDTBit) == str(receivedRDTBit)) and (str(checksumGet(data)) == str(checksum)):
                    self.simulator.u_send(str(self.expectedRDTBit) + str(checksumGet(data)) + data)
                    self.expectedRDTBit = 1 - self.expectedRDTBit

                    sys.stdout.write("{}".format(data))
                    sys.stdout.flush()
                else:
                    negativeRDTBit = str(1 - self.expectedRDTBit)
                    self.simulator.u_send(negativeRDTBit + str(checksumGet(data)) + data)

        except socket.timeout:
            sys.exit()

def checksumGet(data):
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    rcvr = RDTReceiver()
    rcvr.receive()

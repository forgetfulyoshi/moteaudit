#! /usr/bin/python

import argparse
import sys

from mote import *

class WsnSniffer(object):
    def __init__(self, outfile='out.ma'):
        self.registry = MoteRegistry()
        self.outfile = outfile

    def sniff(self):
        self.registry.start()
        sys.stderr.write("[+] Capturing, press Ctrl-C to stop.\n")

        while self.registry.is_running:
            packets = self.registry.dump()
            for packet in packets:
                timestamp = packet[0]
                packet = packet[1]

                breakdown = "Destination: %d" + '\n' \
                            + "Source: %d" + '\n' \
                            + "Length: %d" + '\n' \
                            + "Group: %d" + '\n' \
                            + "Type: %d" + '\n' \
                            + "Data: %s" 

                breakdown = breakdown % (packet.destination,
                                   packet.source,
                                   packet.length,
                                   packet.group,
                                   packet.type,
                                   tos.list2hex(packet.data))

                raw = "%d %s" % (timestamp, tos.list2hex(packet.payload()))
                
                print breakdown + '\n' + raw + '\n\n'

    def stop(self):
        self.registry.is_running = False
        self.registry.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Packet sniffer for WSNs')
    args = parser.parse_args()

    sniffer = WsnSniffer()

    try:
        sniffer.sniff()
    except KeyboardInterrupt:
        sniffer.stop()

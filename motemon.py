#! /usr/bin/python

import argparse
import signal

from mote import *

class WsnSniffer(object):
    def __init__(self, outfile='out.ma'):
        self.registry = MoteRegistry('/dev/ttyUSB1', 57600)
        self.outfile = outfile

    def sniff(self):
        self.registry.start()
        print "[+] Capturing, press Ctrl-C to stop."

    def _stop(self, signal, frame):
        self.registry.is_running = False
        self.registry.join()

        packets = self.registry.packets
        
        with open(self.outfile, 'w') as out:

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
                
                out.write(breakdown + '\n' + raw + '\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Packet sniffer for WSNs')
    
    #TODO
    # Add options
    #   - output file(s)
    #   - comm

    sniffer = WsnSniffer()
    sniffer.sniff()
    signal.signal(signal.SIGINT, sniffer._stop)
    signal.pause()

#! /usr/bin/python

import argparse
import signal

from mote import *

class WsnSniffer(object):
    def __init__(self, outfile=''):
        self.registry = MoteRegistry('/dev/ttyUSB1', 57600)
        self.outfile = outfile

    def sniff(self):
        self.registry.start()
        print "[+] Capturing, press Ctrl-C to stop."

    def _stop(self, signal, frame):
        print "setting to false"
        self.registry.is_running = False
        print "joining"
        self.registry.join()

        print 'getting packets'
        packets = self.registry.packets
        
        print 'opening file'
        with open(self.outfile, 'w') as out:

            for packet in packets:
                out.write(str(packet[0]) + \
                        tos.list2hex(packet[1].payload()) + \
                        '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Packet sniffer for WSNs')
    
    #TODO
    # Add options
    #   - output file(s)
    #   - comm

    sniffer = WsnSniffer('out.mm')
    sniffer.sniff()
    signal.signal(signal.SIGINT, sniffer._stop)
    signal.pause()

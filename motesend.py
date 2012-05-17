#! /usr/bin/python

import argparse

from mote import *

def inject(source, dest, group, payload):
    sender = MoteInjector()
    sender.inject(source, dest, group, payload)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arbitrary packet injection for TinyOS motes")
    parser.add_argument('-s', '--source', type=int, nargs=1, default=[0L],
                        help="Source mote to spoof - default is zero")
    parser.add_argument('-d', '--destination', type=int, nargs=1, default=[0xFFFF],
                        help="Destination for packet - default is flooding")
    parser.add_argument('-g', '--group', type=int, nargs=1, default=[0L],
                        help="Mote group - default is zero")
    parser.add_argument('payload', type=str, nargs=1, default='',
                        help="Packet payload. Should be a comma-separated list \
                        of decimals (e.g. 0,0,1,55)")
    
    args = parser.parse_args()
    
    source = args.source.pop()
    dest = args.destination.pop()
    group = args.group.pop()
    
    try:
        payload = [int(x) for x in args.payload.pop().split(',')]
    except ValueError:
        print "[-] Invalid payload format"
        sys.exit()

    inject(source, dest, group, payload)

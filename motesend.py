#! /usr/bin/python

import argparse

from mote import *

def inject(source, dest, group, payload):
    sender = MoteInjector()
    sender.inject(source, dest, group, payload)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arbitrary packet injection for TinyOS motes")
    parser.add_argument('source', type=int, nargs=1, 
                        help="Source mote to spoof")
    parser.add_argument('destination', type=int, nargs='?', default=0xFFFF,
                        help="Destination for packet - defaults to flooding")
    parser.add_argument('group', type=int, nargs=1,
                        help="Mote group")
    parser.add_argument('payload', type=str, nargs=1, default='',
                        help="Packet payload")
    
    args = parser.parse_args()
    print args
    
    source = args.source.pop()
    dest = args.destination
    group = args.group.pop()
    payload = [int(x) for x in args.payload.pop().split(',')]

    inject(source, dest, group, payload)

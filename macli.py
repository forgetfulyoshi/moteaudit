#! /usr/bin/python

import argparse
import cmd
import os
import signal
import sys

from mote import *

class MoteAuditPrompt(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'moteaudit> '

        self.injector = MoteInjector()

        self.mote_registry = MoteRegistry()
        self.mote_registry.start()

    def do_inject(self, args):
        """send arbitrary data"""
        parser = argparse.ArgumentParser(description='Send arbitrary data')
        parser.add_argument('-d', '--dest', type=int, nargs='?', default=0xFFFF,
                            help="Destination for packet - default is flooding")
        parser.add_argument('-s', '--src', type=int, nargs='?', default=0,
                            help="Source of packet - default is zero")
        parser.add_argument('-g', '--grp', type=int, nargs='?',
                            default=self.mote_registry.group,
                            help="Mote group - known groups are: " + str(self.mote_registry.groups))
        parser.add_argument('payload', type=str, nargs=1,
                            help="Payload for packet")

        try:
            args = parser.parse_args(args.split())
        except SystemExit:
            return

        print args
        dest = args.dest
        source = args.src
        group = args.grp
        payload = [int(x) for x in args.payload.pop().split(',')]

        self.injector.inject(source, dest, group, payload)

    def do_replay(self, args):
        """replay a selected packet"""
        parser = argparse.ArgumentParser(description='Replay any received packet')
        parser.add_argument('packet', type=int, nargs=1, 
                            help="Packet to replay - use ls to see received packets")

        try:
            args = parser.parse_args(args.split())
        except SystemExit:
            return

        packet_id = args.packet.pop()
        packet = None
        for (pid, pkt) in self.mote_registry.packets:
            if pid == packet_id:
                packet = pkt
                break

        if packet != None:
           self.injector.inject(packet.source, packet.destination,
                                packet.group, packet.data)
        else:
            print "[-] Packet not found"

    def do_ls(self, args):
        """get details of a mote"""
        parser = argparse.ArgumentParser(description='List all known motes')
        parser.add_argument('mote_id', type=int, nargs='?',
                            help='Give information for a specifc mote')

        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return

        mote = args.mote_id

        if mote:
            motes = self.mote_registry.summary()
            if mote in motes:
                print str(hex(mote)) + '\t' \
                      + str(motes[mote]['sent']) + '\t' \
                      + str(motes[mote]['recv'])
        
        else:
            motes = self.mote_registry.summary()
            for mote in motes:
                print str(hex(mote)) + '\t' \
                      + str(motes[mote]['sent']) + '\t' \
                      + str(motes[mote]['recv'])


    def do_packets(self, args):
        parser = argparse.ArgumentParser(description='Get a range of packets')
        parser.add_argument('count', type=int, nargs=1,
                            help='Return this many of the most recent packets')

        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return

        count = args.count.pop()

        pkts = self.mote_registry.packets[-count:]
        
        for pkt in pkts:
            print pkt

    def do_clear(self, args):
        os.system('clear')

    def do_exit(self, args):
        self.quit()

    def do_quit(self, args):
        self.quit()

    def default(self, line):
        print "Command not found"

    def catch(self, signal, line):
        self.quit()

    def quit(self, signal=None, frame=None):
        self.mote_registry.is_running = False
        self.mote_registry.join()
        sys.exit()

if __name__ == '__main__':
    prompt = MoteAuditPrompt()
    signal.signal(signal.SIGINT, prompt.quit)
    prompt.cmdloop()

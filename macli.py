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

        self.mote_registry = MoteRegistry('/dev/ttyUSB1', 57600)
        self.mote_registry.start()

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

        pkts = self.mote_registry.packets[:-count]
        
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

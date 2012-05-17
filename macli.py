#! /usr/bin/python

import argparse
import cmd
import os
import sys

from mote import *

class MoteAuditPrompt(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'Welcome to the Mote Audit Command Line Interface (MACLI)'
        self.prompt = 'macli> '

        self.injector = MoteInjector()

        self.mote_registry = MoteRegistry()
        self.mote_registry.start()
        self.onecmd('clear')
    
    def help_inject(self):
        self.do_inject('-h')
    
    def do_inject(self, args):
        """send arbitrary data"""
        parser = argparse.ArgumentParser(prog='inject', description='Send arbitrary data')
        parser.add_argument('-d', '--dest', type=int, nargs=1, default=0xFFFF,
                            help="Destination for packet - default is flooding")
        parser.add_argument('-s', '--src', type=int, nargs=1, default=0,
                            help="Source of packet - default is zero")
        parser.add_argument('-g', '--grp', type=int, nargs=1,
                            default=self.mote_registry.group,
                            help="Mote group - use the groups command for a \
                            listing")
        parser.add_argument('payload', type=str, nargs=1,
                            help="Payload for packet. Format is single decimal \
                            values, separated by commas ( e.g. 0,0,1,50 )")

        try:
            args = parser.parse_args(args.split())
        except SystemExit:
            return

        print args
        dest = args.dest
        source = args.src
        group = args.grp
        
        try:
            payload = [int(x) for x in args.payload.pop().split(',')]
        except ValueError as e:
            print "Invalid payload format"
            return

        self.injector.inject(source, dest, group, payload)

    def help_replay(self):
        self.do_replay('-h')
        
    def do_replay(self, args):
        """replay a selected packet"""
        parser = argparse.ArgumentParser(prog='replay', description='Replay any received packet')
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

    def help_groups(self):
        self.do_groups('-h')

    def do_groups(self, args):
        parser = argparse.ArgumentParser(prog='groups', description='List all \
                                        known groups')
        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return

        print 'Group ID\n----------'
        print '\n'.join([str(i) for i in self.mote_registry.groups])

    def help_ls(self):
        self.do_ls('-h')

    def do_ls(self, args):
        """get details of a mote"""
        parser = argparse.ArgumentParser(prog='ls', description='List all known motes')
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


    def help_packets(self):
        self.do_packets('-h')

    def do_packets(self, args):
        parser = argparse.ArgumentParser(prog='packets', description='Get a range of packets')
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

    def help_clear(self):
        self.do_clear('-h')

    def do_clear(self, args):
        
        parser = argparse.ArgumentParser(prog='clear', description='Clear the screen')
        
        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return

        os.system('clear')

    def help_exit(self):
        self.do_exit('-h')

    def do_exit(self, args):
        parser = argparse.ArgumentParser(prog='exit', description='Exit MACLI')

        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return

        self.quit()

    def help_quit(self):
        self.do_quit('-h')

    def do_quit(self, args):
        parser = argparse.ArgumentParser(prog='quit', description='Exit MACLI')

        try:
            args = parser.parse_args(args.split())
        except SystemExit as e:
            return
        
        self.quit()

    def default(self, line):
        print "Command not found"

    def quit(self):
        self.mote_registry.is_running = False
        self.mote_registry.join()
        self.onecmd('clear')
        sys.exit()

if __name__ == '__main__':
    prompt = MoteAuditPrompt()

    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        prompt.quit()

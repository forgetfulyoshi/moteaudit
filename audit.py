import cmd
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
        args = args.split()
        
        if len(args) is 0:
            motes = self.mote_registry.summary()
            for mote in motes:
                print str(hex(mote)) + '\t' \
                      + str(motes[mote]['sent']) + '\t' \
                      + str(motes[mote]['recv'])

        if len(args) is 1:
            motes = self.mote_registry.summary()
            mote = int(args[0])
            if mote in motes:
                print str(hex(mote)) + '\t' \
                      + str(motes[mote]['sent']) + '\t' \
                      + str(motes[mote]['recv'])

    def do_packets(self, args):
        if len(args) is 1:
            mote = int(args[0])
            pkts = self.mote_registry.packets(mote)
            
            for pkt in pkts:
                print str(pkt) + ') ' + pkts[pkt]

    def do_exit(self, args):
        self.quit()

    def do_quit(self, args):
        self.quit()

    def default(self, line):
        print "Command not found"

    def quit(self):
        self.mote_registry.is_running = False
        self.mote_registry.join()
        sys.exit()

if __name__ == '__main__':
    prompt = MoteAuditPrompt()
    prompt.cmdloop()

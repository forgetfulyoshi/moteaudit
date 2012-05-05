import cmd
import sys

class MoteRegistry(object):
    def __init__(self):
        pass

    def summary(self):
        return "summary placeholder"

    def info(mote_id, field):
        return "info placeholder"

class MoteAuditPrompt(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'moteaudit> '

        self.mote_registry = MoteRegistry()

    def do_ls(self, args):
        """list all known motes"""
        print self.mote_registry.summary()

    def do_mote(self, args):
        """get details of a mote"""
        print args
        args = args.split()
        if len(args) is 2:
            try:
                print self.mote_registry.info(args[0], args[1])
            except Exception:
                print "didn't work"

    def do_exit(self, args):
        self.quit()

    def do_quit(self, args):
        self.quit()

    def default(self, line):
        print "No such command"

    def quit(self):
        sys.exit()

if __name__ == '__main__':
    prompt = MoteAuditPrompt()
    prompt.cmdloop()

import threading
import time
import tos

io_lock = threading.Lock()

class MoteInjector(object):
    def __init__(self, serial=None):
        self.am = tos.AM(s=serial)

    def inject(self, source, dest, group, payload):
        packet = tos.ActiveMessage()

        packet.source = source
        packet.destination = dest
        packet.type = 6L
        packet.group = group
        packet.data = payload
        packet.length = len(payload)
        
        with io_lock:
            self.am.write(packet.payload(), packet.type)

class MoteRegistry(threading.Thread):
    def __init__(self, serial=None):
        threading.Thread.__init__(self)
        
        self.motes = {}
        self.packets = []
        self.groups = []
        self.motes_lock = threading.Lock()
        self.is_running = False
        
        self.active_message = tos.AM(s=serial)

    def _get_group(self):
        if self.groups:
            return self.groups.pop()

        return 0

    group = property(_get_group)

    def run(self):
        self.is_running = True
        packet_count = 0
        while self.is_running:
            
            data = None
            with io_lock:
                data = self.active_message.read(timeout=1)
            
            if data == None:
                continue

            source = int(data.source)
            dest = int(data.destination)
            group = int(data.group)

            if group not in self.groups:
                self.groups.append(group)

            with self.motes_lock:
                if source not in self.motes:
                    new_mote = Mote()
                    new_mote.mote_id = source
                    self.motes[source] = new_mote

                if dest not in self.motes:
                    new_mote = Mote()
                    new_mote.mote_id = dest
                    self.motes[dest] = new_mote

                self.motes[source].num_packets_sent += 1
                self.motes[dest].num_packets_recv += 1
                self.motes[source].add_packet(data)
                self.motes[source].group = group

                self.packets.append((packet_count,  data))
                
                packet_count += 1

    def summary(self):
        with self.motes_lock:
            summary = {}
            for m in self.motes:
                mote = self.motes[m]
                summary[mote.mote_id] = {}
                summary[mote.mote_id]['sent'] = mote.num_packets_sent
                summary[mote.mote_id]['recv'] = mote.num_packets_recv
                
            return summary

    def info(self, mote_id, field):
        value = None
        mote_id = int(mote_id)
        with self.motes_lock:
            if mote_id not in self.motes:
                return None

            try:
                value = getattr(self.motes[mote_id], field)
            except AttributeError:
                return None

            return value
    

    def stop(self):
        self.is_running = False

class Mote(object):
    def __init__(self):
        self.mote_id = -1
        self.num_packets_sent = 0
        self.num_packets_recv = 0
        self.packets = {}
        self._num = 0
        self.group = -1

    def add_packet(self, packet):
        hex_packet = tos.list2hex(packet.payload())

        self.packets[self._num % 10] = hex_packet
        self._num += 1

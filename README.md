# moteaudit #

Auditing tool for wireless sensor networks

## macli ##

Interactive prompt for auditing WSNs. Can be used to:

- Capture packets
- Enumerate all motes
- Inject arbitrary packets
- Replay any captured pacekts
    

## motemon ##

 usage: motemon.py [-h]

 Packet sniffer for TinyOS motes

 optional arguments:
    -h, --help  show this help message and exit

## motesend ##

usage: motesend.py [-h] source [destination] group payload

Arbitrary packet injection for TinyOS motes

positional arguments:
    
    source       Source mote to spoof
    
    destination  Destination for packet - defaults to flooding
    
    group        Mote group
    
    payload      Packet payload

optional arguments:
    -h, --help   show this help message and exit

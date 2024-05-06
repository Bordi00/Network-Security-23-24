from scapy.all import *

target_ip =  # insert target ip

# forge the packet
ip = IP()

# Specify the packet type
icmp = 

# add raw some data
# Remeber the size of the maximum packet length and the allocatated memory by the server
# hint: raw uses bytes)

raw = Raw()


# stack up the layers 
# (hint: use the / operator)


# send the packet and start the attack
# (hint: use fragment() to fragment the packet and loop to continously send packets
send()



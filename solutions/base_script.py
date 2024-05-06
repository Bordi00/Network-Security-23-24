from scapy.all import *

target_ip = "172.18.0.2"
nameserver = "172.18.0.5"
domain = "google.com"

ip = IP(src=target_ip, dst=nameserver)
udp = UDP(dport=53)
dns = DNS(rd=1, qdcount=1, qd=DNSQR(qname=domain, qtype=255))

request = ip/udp/dns

send(request)

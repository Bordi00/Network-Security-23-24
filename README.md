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
During this lab we will use IPv4 since its the most used at the moment. This protocol is described in RFC 791 and the year after it became the standard of the Internet Protocol Suite (TCP/IP). The header consists of 14 fields, of which 13 are required.
<inserire immagine ip header>
The total length of the entire packet size including header and data is 65535 bytes and the minimum size is 20 bytes (header without data). Some of the fields important to us are: fragment offset (since the message can be split in different ip packets), protocol (it can be set to ICMP, TCP, UDP and others) and lastly source and destination address.

#### GNS3
GNS3 is a Graphical Network Simulator created in python and under the GPL license. It will be the environment where the lab will happen to start it open a terminal type gns3 and press enter

<inserire immagine terminale con gns3>

To use our topology select, by double clicking, DoS_lab from the project library tab; to start all the machines press the green play button in the top left. Our topology is divided in two LANs one that contains the attacker (the one in yellow) and a second one that contains the victim (light blue). If you want to interact with any of the elements in the topology just right click it and a drop down menu will appear. For example if you want to open a terminal on the kali-machine-1 (the atacker) right click it and select terminal from the menu. During this lab kali-machine-1 will be us, the attacker, and Victim is the target of our attacks.

### Ping Flood
Ping flood is a volume based attack where we try to take the hole bandwidth for our self by spamming pings to the victim, this will render the server unreachable to any one else. To do so we will use the hping3 on the kali machine using the flag -1 for ICMP and --flood to spamm ping messages. To see the result of our attaks we will first start a ping from PC1 towards the victim with the command:

`ping 192.168.100.18 -t`

the flag -t here is to continuosly ping the server; if it will ever go down we will see a timeout in the logs. To start the attack we open the shell on the kali machine and use the command:

`hping3 -1 --flood 192.168.100.18`

once we start the command we can see that the pings from PC1 won't be received from the victim this can also be seen if we click on the connection between the router and the server and open wireshark there. To make this attack less detectable we can add the flag --rand-source To end the attak just press Ctrl+c on the kali shell and you will see that the pings will be recived by the server once again.

### Ping of death
Ping of death is a resource based attack with the goal to crash a server due to it allocating too little space for the recived package. As already mantion the maximun leangth of a ping is 65535 with 20 used by the header but in many older versions of OSs the allocated space is way less (e.g. one datagram which is 1500 bytes); this oversite was repeated even in IPv6. For our exercise open the terminal on kali-machine-1 and edit the unfinished version of ping_of_death.py with either vim or nano. One possible solution is:

`from scapy.all import *
target_ip = None # insert target ip
ip = IP(dst=target_ip)
icmp = ICMP()
raw = Raw(b'X'*65500)
packet = ip / icmp / raw
send(fragment(packet), loop=1, verbose=0)`

To check if the scrip is correct lounch it with the command

`python ping_of_death.py`

and see if the ping from the PC1 don't reach the victim

### Mitigations
The mitigation very from more to less extreme and are:
- Not allow ping at all
- Have Access Control Lists
  - They can check if the same IP is tring to send too many packeges
  - They can see if the IP is well formed
- Use firewalls
  - It can see if the content of the ping is larger than expected 

## Transport Layer DoS attacks
### TCP recap
The transport layer [2](#references) ensures reliable, error-free delivery of data between end systems, such as computers or servers. It also provides mechanisms for error detection, flow control, and congestion avoidance and manages the transmission of messages from layers 1 through 3.

These attacks target the transport layer (layer 4) of the OSI model, with the goal of overloading the target’s servers or network devices. Transport layer DDoS attacks include SYN (synchronization) floods, TCP (Transmission Control Protocol) floods, and UDP (User Datagram Protocol) floods. Transport layer attacks can result in the limiting of reach bandwidth or connections of hosts or networking equipment.

### SYN flood 

### Mitigations

## Application Layer attacks
### HTTP recap

### HTTP flood

### RUDY attack

### Slowloris attack

### Mitigations

## DDoS attacks

### DoS vs. DDoS

### DNS Amplification attack

### Mitigations

## References
1. [What is a denial of service attack (DoS) ?](https://www.paloaltonetworks.com/cyberpedia/what-is-a-denial-of-service-attack-dos)
2. [Transport Layer DoS attacks](https://www.cdnetworks.com/cloud-security-blog/types-of-ddos-attacks/#:~:text=Transport%20Layer%20DDoS%20attacks&text=These%20attacks%20target%20the%20transport,(User%20Datagram%20Protocol)%20floods.)

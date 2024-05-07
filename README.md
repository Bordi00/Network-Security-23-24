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
There are two main types of DoS attacks one is volume based and the other one is resource based. This tow are also known as flood an crash based respectively. The difference between the two is in how they deplete the resources of the target: the first one (flood) tries to take as much resources of the target as possible, the other one (crash) tries to crash the server thus rendering it unreachable through bug or bad implementation of protocols.

## Network Layer DoS attacks
The network layer provides the means of transferring variable-length network packets from a source to a destination host via one or more networks. This layer responds to service request from the transport layer and issues service requests to the data link layer. We will analyze the IP protocols and how this non secure protocol can be exploited by a malicious user.

### IP recap
During this lab we will use IPv4 since its the most used at the moment. This protocol is described in RFC 791 and the year after it became the standard of the Internet Protocol Suite (TCP/IP). The header consists of 14 fields, of which 13 are required.
<inserire immagine ip header>
The total length of the entire packet size including header and data is 65535 bytes and the minimum size is 20 bytes (header without data). Some of the fields important to us are: fragment offset (since the message can be split in different ip packets), protocol (it can be set to ICMP, TCP, UDP and others) and lastly source and destination address.

### Ping Flood 
Ping flood is a volume based attack where we try to take the hole bandwidth for our self by spamming pings to the victim, this will render the server unreachable to any one else. To do so we will use the hping3 command but first we need to set up the environment.

#### GNS3
GNS3 is a Graphical Network Simulator created in python and under the GPL license. To start it open a terminal type gns3 and press enter
<inserire immagine terminale con gns3>
To use our topology select 
### Ping of death
### Mitigations

## Transport Layer DoS attacks
### TCP recap

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

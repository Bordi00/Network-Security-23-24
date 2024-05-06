FROM kalilinux/kali-rolling:latest

RUN apt-get update && apt-get install -y \
	net-tools \
	iputils-ping \
	python3 \
	python3-pip \
	hping3 \
	vim \
	nano \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install scapy requests

ADD "scripts/syn_flood.py" "syn_flood.py"
ADD "scripts/ping_of_death.py" "ping_of_death.py"
ADD "scripts/slowloris.py" "slowloris.py"
ADD "scripts/rudy.py" "rudy.py"
ADD "scripts/pyflooder2.py" "pyflooder2.py"

RUN chmod a+x syn_flood.py
RUN chmod a+x ping_of_death.py
RUN chmod a+x slowloris.py
RUN chmod a+x rudy.py
RUN chmod a+x pyflooder2.py
RUN chmod a+x slowloris.py

CMD ["bash"]

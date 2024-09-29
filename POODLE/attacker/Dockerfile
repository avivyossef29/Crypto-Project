
FROM mitmproxy/mitmproxy:8.0.0

# RUN apt-get update && \
#     apt-get install -y python3-pip iproute2 iputils-ping && \
#     pip3 install scapy

# COPY ./attacker.py /attacker.py

# EXPOSE 8080

# CMD ["mitmdump", "-p", "8080", "--ssl-insecure", "--allow-hosts", "server_container", "-s", "/attacker.py"]



FROM python:3.5.3-alpine3.4

RUN apk --no-cache add curl libnfnetlink-dev libnetfilter-queue-dev

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org requests==2.5.0 urllib3==1.10 scapy NetfilterQueue==0.9
COPY ./attacker.py /attacker.py

EXPOSE 8080

CMD ["python", "-u", "attacker.py"]
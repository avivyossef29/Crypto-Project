FROM python:3.5.3-alpine3.4

RUN apk --no-cache add bash

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org requests==2.5.0 urllib3==1.10 scapy==2.4.0 libpcap

COPY . .

RUN export PYTHONWARNINGS="ignore:Unverified HTTPS request"

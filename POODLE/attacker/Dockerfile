FROM python:3.5.3-alpine3.4

RUN apk --no-cache add curl

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org requests==2.5.0 urllib3==1.10 scapy

COPY ./attacker.py /attacker.py

CMD ["python", "-u", "attacker.py"]
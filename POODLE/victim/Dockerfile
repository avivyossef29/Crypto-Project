FROM python:3.5.3-alpine3.4

RUN apk --no-cache add curl

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org requests==2.5.0 urllib3==1.10

COPY ./script.py /script.py

RUN export PYTHONWARNINGS="ignore:Unverified HTTPS request"

CMD ["python", "script.py"]

# Run the connection script
#CMD ["curl", "--sslv3", "--insecure", "--ciphers", "AES128-SHA", "https://server-demo/"]
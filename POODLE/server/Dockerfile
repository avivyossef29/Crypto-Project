FROM python:3.5.3-alpine3.4

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org flask==1.1.0

WORKDIR /server

COPY ./server.py /server/server.py

COPY ./server.crt /server/server.crt
COPY ./server.key /server/server.key

EXPOSE 443

ENTRYPOINT [ "python" ]

CMD ["server.py"]
FROM python:3.5.3-alpine3.4

RUN pip install -U pip

RUN pip install --trusted-host pypi.python.org requests==2.5.0 urllib3==1.10

COPY ./victim.py /victim.py

RUN export PYTHONWARNINGS="ignore:Unverified HTTPS request"

CMD ["python", "victim.py"]

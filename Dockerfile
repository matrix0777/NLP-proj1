FROM python:3.7-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /web

COPY . /web
RUN pip install -r requirements.txt

CMD ["python3", "web.py"]
FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    dpkg \
    dumb-init \
    wireguard-tools \
    iptables

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

CMD ["python", "run.py"]
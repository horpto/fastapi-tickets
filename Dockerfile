FROM python:3.10-slim

EXPOSE 8080

COPY requirements.txt .

RUN apt update \
    && apt install -y gcc \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt purge -y gcc \
    && apt clean -y && apt autoremove -y

ADD . /opt/tickets

WORKDIR /opt/tickets/

# Run Api
CMD [ "python3", "main.py" ]

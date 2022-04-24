FROM python:3.10-slim

EXPOSE 8080

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

ADD . /opt/tickets

WORKDIR /opt/tickets/

# Run Api
CMD [ "python3", "main.py" ]

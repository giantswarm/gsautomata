FROM python:3.9.1-slim

COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT python main.py

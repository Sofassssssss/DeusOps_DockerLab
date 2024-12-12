FROM python:3.10-alpine
LABEL authors="sofiavovchenko"

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/static /app/templates

RUN addgroup -S notroot && adduser -S imnotroot -G notroot
USER imnotroot

CMD alembic upgrade head && python main.py


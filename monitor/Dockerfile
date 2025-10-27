FROM alpine:latest

WORKDIR /monitor

RUN apk update && \
    apk add --no-cache python3 py3-pip iputils py3-redis py3-yaml py3-flask

COPY . /monitor

CMD ["python3", "-u", "app.py"]
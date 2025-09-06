FROM alpine:latest

WORKDIR /app

# Install Python, pip, ping, redis, and yaml libraries
RUN apk update && \
    apk add --no-cache python3 py3-pip iputils py3-redis py3-yaml

COPY . /app

CMD ["python3", "-u", "app.py"]
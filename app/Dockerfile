FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping
CMD ["python", "app.py"]


import subprocess
from settings import Setup
import time
import threading
import redis
import json

class App:
    def __init__(self):
        self.timeout, self.totens, self.paineis = Setup().import_settings()
        self.conn = redis.Redis(host='redis', port=6379, db=0)
        # Check Redis connection
        try:
            self.conn.ping()    
            print("Connected to Redis server successfully.")
        except redis.ConnectionError:
            print("Redis server is not running. Please start the Redis server and try again.")
            exit(1)


    def isOnline(self, hosts, category):
        for host in hosts:
            command = ["ping", "-c", "3", "-W", "1", host]
            response = subprocess.run(command, capture_output=True, text=True)
            status = 0 if response.returncode == 0 else 1
            ip = hosts[host][0]
            
            try:
                data = {
                    "ip": ip,
                    "hostname": host,
                    "status": status,
                }

                if category == 'painel':
                    self.conn.hset("PAINEL_STATUS", host, json.dumps(data))
                elif category == 'totem':
                    self.conn.hset("TOTEM_STATUS", host, json.dumps(data))

            except Exception as a:
                print(f"Error: it couldn't record on redis db", a)

    def run(self):
        while True:
            self.conn.expire("PAINEL_STATUS", self.timeout)
            self.conn.expire("TOTEM_STATUS", self.timeout)
            t1 = threading.Thread(target=self.isOnline, args=(self.totens, 'totem'))
            t2 = threading.Thread(target=self.isOnline, args=(self.paineis, 'painel'))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            time.sleep(self.timeout)

if __name__ == "__main__":
    app = App()
    app.run()
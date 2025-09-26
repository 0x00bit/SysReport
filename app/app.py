import subprocess
from settings import Setup
import time
import threading
import redis

class App:
    def __init__(self):
        self.timeout, self.hosts = Setup().import_settings()
        self.conn = redis.Redis(host='redis', port=6379, db=0)
        # Check Redis connection
        try:
            self.conn.ping()    
            print("Connected to Redis server successfully.")
        except redis.ConnectionError:
            print("Redis server is not running. Please start the Redis server and try again.")
            exit(1)

        self.totens = self.hosts['totens']
        self.panels = self.hosts['paineis']

    def isOnline(self, hosts, category):
        for host in hosts:
            command = ["ping", "-c", "3", "-W", "1", host]
            response = subprocess.run(command, capture_output=True, text=True)
            status = 1 if response.returncode == 0 else 0
            
            try:
                if category == 'painel':
                    self.conn.hset("PAINEL_STATUS", host, status)
                elif category == 'totem':
                    self.conn.hset("TOTEM_STATUS", host, status)
            except Exception as a:
                print(f"Error: it couldn't record on redis db", a)

    def run(self):
        while True:
            self.conn.expire("PAINEL_STATUS", self.timeout)
            self.conn.expire("TOTEM_STATUS", self.timeout)
            t1 = threading.Thread(target=self.isOnline, args=(self.totens, 'totem'))
            t2 = threading.Thread(target=self.isOnline, args=(self.panels, 'painel'))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            time.sleep(self.timeout)

if __name__ == "__main__":
    app = App()
    app.run()
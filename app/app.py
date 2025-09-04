import subprocess
from settings import Setup
import time
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
        self.panels = self.hosts['panels']

        # # Running devices lists
        self.totens_online_hosts = []
        self.panels_online_hosts = []

        self.totens_offline_hosts = []
        self.panels_offline_hosts = []

    def isOnline(self, hosts, category):

        for host in hosts:
            command = ["ping", "-c", "1", "-W", "1", host]
            response = subprocess.run(command, capture_output=True, text=True)

            status = 'UP' if response.returncode == 0 else 'DOWN'
            
            try:
                if category == 'panel':
                    self.conn.hset("PAINEL_STATUS", host, status)
                elif category == 'totem':
                    self.conn.hset("TOTEM_STATUS", host, status)
            except Exception as a:
                print(f"erro ao gravar no redis", a)

    def run(self):
        while True:
    
            self.totens_online_hosts.clear()
            self.totens_offline_hosts.clear()
            self.panels_online_hosts.clear()
            self.panels_offline_hosts.clear()

            self.isOnline(self.totens, 'totem')

            self.isOnline(self.panels, 'panel')

            time.sleep(int(self.timeout) / 1000)
        
if __name__ == "__main__":
    app = App()
    app.run()

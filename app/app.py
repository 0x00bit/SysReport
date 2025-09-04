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
            command = ["ping", "-n", "3", "-w", "1000", host]
            response = subprocess.run(command, capture_output=True, text=True)
            
            if response.returncode == 0:
                if category == 'panel':
                    self.panels_online_hosts.append(host)
                elif category == 'totem':
                    self.totens_online_hosts.append(host)

            else:
                if category == 'panel':
                    self.panels_offline_hosts.append(host)
                elif category == 'totem':
                    self.totens_offline_hosts.append(host)

    def run(self):
        while True:
            # Limpa as listas antes de cada rodada
            self.totens_online_hosts.clear()
            self.totens_offline_hosts.clear()
            self.panels_online_hosts.clear()
            self.panels_offline_hosts.clear()

            self.isOnline(self.totens, 'totem')

            try:
                self.conn.set('TOTEM UP', ','.join(self.totens_online_hosts))
                self.conn.set('TOTEM DOWN', ','.join(self.totens_offline_hosts))
            except Exception as e:
                print("Error setting Redis keys:", e)

            print("DEBUGGING> Totens Online:", self.totens_online_hosts)

            self.isOnline(self.panels, 'panel')
            try:
                self.conn.set('PAINEL UP', ','.join(self.panels_online_hosts))
                self.conn.set('PAINEL DOWN', ','.join(self.panels_offline_hosts))
            except Exception as e:
                print("Error setting Redis keys:", e)
            print("Paineis Online:", self.panels_online_hosts)

            time.sleep(int(self.timeout) / 1000)
        
if __name__ == "__main__":
    app = App()
    app.run()

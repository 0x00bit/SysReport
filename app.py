import subprocess
from settings import Setup
import time

class App:
    def __init__(self):
        self.timeout, self.hosts = Setup().import_settings()

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
            self.isOnline(self.totens, 'totem')
            print("Totens Online:", self.totens_online_hosts)
            self.isOnline(self.panels, 'panel')
            print("Panels Online:", self.panels_online_hosts)
            time.sleep(int(self.timeout) / 1000)
        
if __name__ == "__main__":
    app = App()
    app.run()

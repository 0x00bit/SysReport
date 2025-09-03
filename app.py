import subprocess
from settings import Setup
import wmi

class App:
    def __init__(self):
        self.username, self.raw_password, self.hosts = Setup().import_settings()
        self.decoded_password = Setup().getPassword(self.raw_password)

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

    def checkProcess(self, hosts, process):
        for host in hosts:
            conn = wmi.WMI(computer=host, user="HAPVIDA", password="cpdh@p")
            for process in conn.Win32_Process():
                if "msedge.exe" in process.Name.lower():
                    print("deu bom")

    def run(self):
        print(self.hosts['totens'])
        self.isOnline(self.hosts['totens'], 'totem')
        print(self.totens_online_hosts)

if __name__ == "__main__":
    app = App()
    app.run()

import subprocess
from settings import Setup

class App:
    def __init__(self):
        self.username, self.raw_password, self.hosts = Setup().import_settings()
        self.decoded_password = Setup().getPassword(self.raw_password)

        self.totens = self.hosts.get('totens', [])
        self.panels = self.hosts.get('panels', [])

        # Running devices lists
        self.totens_online_hosts = []
        self.panels_online_hosts = []

        self.totens_offline_hosts = []
        self.panels_offline_hosts = []

    def isOnline(self, onlisttype, offlisttype):

        for host in self.hosts:
            command = ["ping", "-n", "3", "-w", "1000", host]
            response = subprocess.run(command, capture_output=True, text=True)
            if response.returncode == 0:
                onlisttype.append(host)
                print(f"{host} is online")
            else:
                offlisttype.append(host)
                print(f"{host} is offline")

    def run(self):
        print("Checking Totens...")
        self.isOnline(self.totens_online_hosts, self.totens_offline_hosts)

        print("\nChecking Panels...")
        self.isOnline(self.panels_online_hosts, self.panels_offline_hosts)

        print("\nTotens Online:", self.totens_online_hosts)
        print("Totens Offline:", self.totens_offline_hosts)

        print("\nPanels Online:", self.panels_online_hosts)
        print("Panels Offline:", self.panels_offline_hosts)


if __name__ == "__main__":
    app = App()
    app.run()

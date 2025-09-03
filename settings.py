import yaml
import base64

class Setup:
    """Class for importing settings from a YAML file."""

    def import_settings(self):
        try:
            with open('settings.yaml', 'r') as file:
                settings = yaml.safe_load(file)
                return settings.get('username'), settings.get('password'), settings.get('hosts', [])
    
        except FileNotFoundError:
            print("Settings file not found.")
            return 1
    
    def getPassword(self, password):
        if password:
            decoded_bytes = base64.b64decode(password)
            return decoded_bytes.decode('utf-8')
    

import yaml
import base64
import os

class Setup:
    """Class for importing settings from a YAML file."""

    def import_settings(self):
        try:
            path = os.path.join(os.path.dirname(__file__), 'settings.yaml')
            with open(path, 'r') as file:
                settings = yaml.safe_load(file)
                return settings.get('timeout'), settings.get('hosts', [])
        except FileNotFoundError as e:
            print(f"Settings file not found. {e}")
            return 1

    

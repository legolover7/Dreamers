import json

from common.classes.globals import FilePaths

def save_terms():
    pass

def save_settings(settings_data):
    """Saves data to the settings file"""
    with open(FilePaths.settings, "w") as outfile:
        outfile.write(json.dumps(settings_data, indent=4))

def save_dreams(dream_data):
    with open(FilePaths.logs, "w") as outfile:
        outfile.write(json.dumps(dream_data, indent=4))
        
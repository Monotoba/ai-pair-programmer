import os
from configparser import ConfigParser


class AIPairProgrammerSettings:
    def __init__(self, filename: str = 'settings.ini'):
        self.filename = filename
        self.config = ConfigParser()
        self.api_key = ""
        self.model_name = ""

    def settings_filename(self, filename: str):
        self.filename = filename

    def getState(self):
        return self

    def loadState(self):
        # Set some defaults
        self.config['api'] = {'key': ''}
        self.config['model'] = {'name': 'davinci'}

        if os.path.isfile(self.filename):
            # Read the settings file
            self.config.read(self.filename)
        else:
            # Create a new settings file with default values
            with open(self.filename, 'w') as ofh:
                self.config.write(ofh)
        self.api_key = self.config.get(section='api', option='key')
        self.model_name = self.config.get(section='model', option='name')

    def saveState(self):
        self.config['api'] = {'key': self.api_key}
        self.config['model'] = {'name': self.model_name}
        # self.config.set(section='api', option='api_key', value=self.api_key)
        # self.config.set(section='model', option='name', value=self.model_name)
        with open(self.filename, 'w') as ofh:
            self.config.write(ofh)

    def get_api_key(self):
        return self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_model_name(self):
        return self.model_name

    def set_model_name(self, model_name):
        self.model_name = model_name

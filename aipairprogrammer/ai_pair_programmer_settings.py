import os
from configparser import ConfigParser


class AIPairProgrammerSettings:
    def __init__(self, filename: str = 'settings.ini'):
        self.filename = filename
        self.config = ConfigParser()
        self._api_key = ""
        self._model_name = ""

    def settings_filename(self, filename: str):
        self.filename = filename

    def get_state(self):
        return self

    def load_state(self):
        # Set some defaults in case file doesn't exist
        self.config['api'] = {'key': '<your api key here>'}
        self.config['model'] = {'name': 'davinci'}

        if os.path.isfile(self.filename):
            # Read the settings file
            self.config.read(self.filename)
        else:
            # No settings file exists, So create a new settings file with default values
            with open(self.filename, 'w') as ofh:
                self.config.write(ofh)
        # Retrieve the settings
        self._api_key = self.config.get(section='api', option='key')
        self._model_name = self.config.get(section='model', option='name')

    def save_state(self):
        self.config['api'] = {'key': self._api_key}
        self.config['model'] = {'name': self._model_name}
        # self.config.set(section='api', option='api_key', value=self.api_key)
        # self.config.set(section='model', option='name', value=self.model_name)
        with open(self.filename, 'w') as ofh:
            self.config.write(ofh)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        self._model_name = model_name

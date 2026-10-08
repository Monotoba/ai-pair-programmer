from io import StringIO
from pathlib import Path

from .persistence import atomic_write, data_directory
from configparser import ConfigParser


class AIPairProgrammerSettings:
    def __init__(self, filename=None):
        self.filename = filename if filename is not None else data_directory() / 'settings.ini'
        self.config = ConfigParser(interpolation=None)
        self._api_key = ""
        self._model_name = ""

    def settings_filename(self, filename: str):
        self.filename = filename

    def get_state(self):
        return self

    def load_state(self):
        self.config = ConfigParser(interpolation=None)
        self.config['model'] = {'name': ''}
        if Path(self.filename).is_file():
            self.config.read(self.filename, encoding='utf-8')
        self._api_key = ''
        self._model_name = self.config.get('model', 'name', fallback='')
        # Explicitly supplied legacy files may contain a key. Never use or rewrite
        # that secret automatically; saving settings removes the old key section.
        if not Path(self.filename).exists():
            self.save_state()

    def save_state(self):
        self.config = ConfigParser(interpolation=None)
        self.config['model'] = {'name': self._model_name}
        output = StringIO()
        self.config.write(output)
        atomic_write(self.filename, output.getvalue())

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

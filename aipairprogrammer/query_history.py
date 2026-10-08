import datetime
import json

from .persistence import atomic_write, data_directory
from pathlib import Path


class HistoryItem:
    def __init__(self, date: str, query: str, response: str):
        self.date: str = date
        self.query: str = query
        self.response: str = response


class QueryHistory:
    def __init__(self, filename=None):
        self.history: list[HistoryItem] = []
        self.current_index = 0
        self.history_filename = filename if filename is not None else data_directory() / 'history.json'
        self._save_blocked = False

    def add(self, query: str, response: str):
        # Creates a HistoryItem and adds
        # it to the end of history list
        now = datetime.datetime.now()
        date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
        item = HistoryItem(date_time_string, query, response)
        self.history.append(item)

    def add_item(self, item: HistoryItem):
        # Adds history item to beginning of history queue
        self.history.append(item)

    def count(self):
        return len(self.history)

    def limit(self, index):
        if len(self.history) == 0:
            index = 0
        elif index >= len(self.history):
            index = len(self.history) - 1
        elif index < 0:
            index = 0
        return index

    def is_in_bounds(self, index):
        result = True
        if len(self.history) == 0:
            result = False
        elif index >= len(self.history):
            result = False
        elif index < 0:
            result = False
        return result

    def first(self):
        # Returns the last item added to the history
        self.current_index = 0
        self.current_index = self.limit(self.current_index)
        if self.is_in_bounds(self.current_index):
            return self.history[self.current_index]
        else:
            return None

    def last(self):
        # returns the first item added to the history
        self.current_index = len(self.history) - 1
        self.current_index = self.limit(self.current_index)
        if self.is_in_bounds(self.current_index):
            return self.history[self.current_index]
        else:
            return None

    def next(self):
        # Returns the next item from history
        self.current_index += 1
        self.current_index = self.limit(self.current_index)
        if self.is_in_bounds(self.current_index):
            return self.history[self.current_index]
        else:
            return None

    def prev(self):
        # Returns the previous item from history
        self.current_index -= 1
        # limit index bounds to
        self.current_index = self.limit(self.current_index)
        if self.is_in_bounds(self.current_index):
            return self.history[self.current_index]
        else:
            return None

    def clear(self):
        # Use with caution!
        # Removes all items from the history
        self.history = []
        self.current_index = 0

    def save_history(self):
        if self._save_blocked:
            raise ValueError('Existing history could not be read; saving is blocked.')
        payload = {'version': 1, 'items': [
            {'date': item.date, 'query': item.query, 'response': item.response}
            for item in self.history
        ]}
        self._validate(payload)
        atomic_write(self.history_filename, json.dumps(payload, ensure_ascii=False, indent=2))

    @staticmethod
    def _validate(payload):
        if (not isinstance(payload, dict) or set(payload) != {'version', 'items'}
                or type(payload['version']) is not int or payload['version'] != 1
                or not isinstance(payload['items'], list)):
            raise ValueError('Unsupported history format.')
        items = []
        for item in payload['items']:
            if (not isinstance(item, dict) or set(item) != {'date', 'query', 'response'}
                    or any(not isinstance(value, str) for value in item.values())):
                raise ValueError('Invalid history item.')
            items.append(HistoryItem(**item))
        return items

    def load_history(self):
        filename = Path(self.history_filename)
        self._save_blocked = True
        if filename.exists():
            with filename.open('r', encoding='utf-8') as stream:
                items = self._validate(json.load(stream))
        else:
            items = []
        self.history = items
        self.current_index = self.limit(self.current_index)
        self._save_blocked = False

import datetime
import pickle
import os


class HistoryItem:
    def __init__(self, date: str, query: str, response: str):
        self.date: str = date
        self.query: str = query
        self.response: str = response


class QueryHistory:
    def __init__(self, filename="history.dat"):
        self.history: list[HistoryItem] = []
        self.current_index = 0
        self.history_filename = filename

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
        cwd = os.getcwd()
        filename = f"{cwd}/{self.history_filename}"
        with open(filename, 'wb') as ofh:
            pickle.dump(self.history, ofh)

    def load_history(self):
        cwd = os.getcwd()
        filename = f"{cwd}/{self.history_filename}"
        if os.path.exists(filename):
            with open(self.history_filename, 'rb') as ifh:
                self.history = pickle.load(ifh)
        else:
            # No history file so, initialize an empty history dict.
            self.history = {}

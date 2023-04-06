import datetime
import pickle


class HistoryItem:
    def __init__(self, date: str, query: str, response: str):
        self.date: str = date
        self.query: str = query
        self.response: str = response


class QueryHistory:
    def __init__(self):
        self.history: list[HistoryItem] = []
        self.current_index = 0
        self.history_filename = 'aipairprogrammer.hist'

    def add(self, query: str, response: str):
        # Adds history to end of history list
        now = datetime.datetime.now()
        date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
        item = HistoryItem(date_time_string, query, response)
        self.history.append(item)

    def addItem(self, item: HistoryItem):
        # Adds history item to beginning of history queue
        self.history.append(item)

    def next(self):
        self.current_index += 1
        if self.current_index >= len(self.history):
            self.current_index = len(self.history) - 1
            print(f'History Index: {self.current_index}, len: {len(self.history)}')
            return None
        else:
            print(f'History Index: {self.current_index}, len: {len(self.history)}')
            return self.history[self.current_index]

    def prev(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
            print(f'History Index: {self.current_index}, len: {len(self.history)}')
            return None
        else:
            print(f'History Index: {self.current_index}, len: {len(self.history)}')
            return self.history[self.current_index]

    def saveHistory(self):
        with open(self.history_filename, 'wb') as ofh:
            pickle.dump(self.history, ofh)

    def loadHistory(self):
        with open(self.history_filename, 'rb') as ifh:
            self.history = pickle.load(ifh)

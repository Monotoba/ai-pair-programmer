import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QDialog, QComboBox, QLineEdit

from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings
from aipairprogrammer.qt_custom_dialog import CustomDialog
from aipairprogrammer.query_history import QueryHistory
from aipairprogrammer.api_client import execute_query


class QueryWorker(QThread):
    result_ready = pyqtSignal(str, bool)

    def __init__(self, query, model, api_key, parent=None):
        super().__init__(parent)
        self.query = query
        self.model = model
        self.api_key = api_key

    def run(self):
        if self.isInterruptionRequested():
            return
        try:
            text, succeeded = execute_query(self.query, self.model, self.api_key)
        except Exception:
            text, succeeded = 'Error: The request failed unexpectedly.', False
        if not self.isInterruptionRequested():
            self.result_ready.emit(text, succeeded)


class AIPairProgrammer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = AIPairProgrammerSettings()
        self.api_key = ''
        self.current_model = ''
        self._query_succeeded = False
        self._request = None
        self._request_cancelled = False
        self._close_when_finished = False
        self.historian = QueryHistory()
        self.init_system()
        self.init_ui()

    def init_system(self):
        self.settings.load_state()
        self.api_key = self.settings.api_key
        self.current_model = self.settings.model_name

    def init_ui(self):
        # Query Edit Box
        query_label = QLabel("Enter your query:")
        self.query_edit = QTextEdit()
        self.query_edit.setFixedHeight(75)

        # ChatGPT Model Selection
        model_label = QLabel("Select a model:")
        self.model_combo_box = QComboBox()
        self.model_combo_box.setEditable(True)
        self.model_combo_box.setInsertPolicy(QComboBox.NoInsert)
        self.model_combo_box.lineEdit().setPlaceholderText('Enter a model ID available to your API account')
        if self.current_model:
            self.model_combo_box.addItem(self.current_model)
        self.model_combo_box.setCurrentText(self.current_model)
        self.model_combo_box.currentTextChanged.connect(self.update_model)

        # ChatGPT Response Text
        self.response_label = QLabel("Response:")
        self.response_edit = QTextEdit()
        self.response_edit.setReadOnly(True)

        # Bottom Button Bar
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_query)

        self.cancel_button = QPushButton("Cancel request")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_request)
        self.request_status = QLabel("Ready")

        clear_button = QPushButton("Clear Text")
        clear_button.clicked.connect(self.clear_text)

        self.config_button = QPushButton("Config")
        self.config_button.clicked.connect(self.show_config_dialog)

        # History
        history_layout = QHBoxLayout()
        history_label = QLabel("History")

        prev_button = QPushButton('Prev')
        prev_button.clicked.connect(self.prev)

        next_button = QPushButton('Next')
        next_button.clicked.connect(self.next)

        # --------------------------------------
        # Final Layout
        # --------------------------------------
        layout = QVBoxLayout()
        layout.addWidget(model_label)
        layout.addWidget(self.model_combo_box)

        # History
        layout.addWidget(history_label)
        history_layout.addWidget(prev_button)
        history_layout.addWidget(next_button)
        layout.addLayout(history_layout)

        # Response
        layout.addWidget(self.response_label)
        layout.addWidget(self.response_edit)
        layout.addWidget(query_label)
        layout.addWidget(self.query_edit)

        layout.addWidget(self.request_status)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(self.config_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_model(self, model_name):
        self.current_model = model_name.strip()
        self.settings.model_name = self.current_model
        self.settings.save_state()

    def _request_inputs(self, query):
        api_key = os.environ.get('OPENAI_API_KEY', '').strip() or self.api_key.strip()
        if not api_key or api_key == '<your api key here>':
            return None, 'You must set your API key before querying the API.'
        if not self.current_model.strip():
            return None, 'Enter a model ID available to your OpenAI API account.'
        if not query.strip():
            return None, 'Please enter a query.'
        return (query, self.current_model.strip(), api_key), None

    def send_query(self):
        if self._request is not None:
            return
        inputs, error = self._request_inputs(self.query_edit.toPlainText())
        if error:
            self.add_response_text(error)
            return
        self._request_cancelled = False
        self._request = QueryWorker(*inputs, parent=self)
        self._request.result_ready.connect(self._receive_result)
        self._request.finished.connect(self._request_finished)
        self.send_button.setEnabled(False)
        self.config_button.setEnabled(False)
        self.model_combo_box.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.request_status.setText('Waiting for response…')
        self._request.start()

    def _receive_result(self, text, succeeded):
        if self._request is None or self._request_cancelled:
            return
        if succeeded:
            self.historian.add(query=self._request.query, response=text)
            saved = self.save_history()
        self.add_response_text(text)
        self.request_status.setText(
            ('Response received' if saved else 'Response received; history not saved')
            if succeeded else 'Request failed')

    def cancel_request(self):
        if self._request is not None:
            self._request_cancelled = True
            self._request.requestInterruption()
            self.cancel_button.setEnabled(False)
            self.request_status.setText('Cancelling locally; waiting for the request to finish…')

    def _request_finished(self):
        worker = self._request
        cancelled = self._request_cancelled
        self._request = None
        worker.deleteLater()
        self.send_button.setEnabled(True)
        self.config_button.setEnabled(True)
        self.model_combo_box.setEnabled(True)
        self.cancel_button.setEnabled(False)
        if cancelled:
            self.request_status.setText('Request cancelled locally')
        if self._close_when_finished:
            self.close()

    def closeEvent(self, event):
        # Keep the widget/thread alive until blocking I/O finishes. Never
        # terminate a thread while it may be using the SDK transport.
        if self._request is not None:
            self._close_when_finished = True
            self.cancel_request()
            event.ignore()
        else:
            super().closeEvent(event)

    def query_gpt(self, query) -> str:
        """Synchronous compatibility helper for scripts and offline tests."""
        self._query_succeeded = False
        inputs, error = self._request_inputs(query)
        if error:
            return error
        text, self._query_succeeded = execute_query(*inputs)
        return text

    def add_response_text(self, new_text: str = ''):
        curr_text = self.response_edit.toPlainText()
        if curr_text and new_text:
            update_text = curr_text + new_text + '\n\n'
        else:
            if new_text:
                update_text = '' + new_text + '\n\n'
            else:
                update_text = ''
        self.response_edit.setPlainText(update_text)
        # Scroll to end of text
        cursor = self.response_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.response_edit.setTextCursor(cursor)

    def clear_text(self):
        self.response_edit.setPlainText('')
        self.query_edit.setPlainText('')

    def prev(self):
        # Previous historical query & response
        item = self.historian.prev()
        if item is not None:
            item_text = item.date + '\n'
            item_text += item.response + '\n\n'
            self.add_response_text(item_text)

    def next(self):
        # Next historical query & response
        item = self.historian.next()
        if item is not None:
            item_text = item.date + '\n'
            item_text += item.response + '\n\n'
            self.add_response_text(item_text)

    def show_config_dialog(self):
        # Show current API Key dialog
        dialog = CustomDialog(title='API configuration',
                              prompt='Enter your OpenAI API key:',
                              placeholderText='Session API key',
                              noteText='The key is used for this session only. Use OPENAI_API_KEY for future launches.')
        dialog.input_field.setEchoMode(QLineEdit.Password)
        # dialog.setTextValue('This is a test')
        ok = dialog.exec()
        if ok == QDialog.Accepted:
            api_key = dialog.input_field.text()
            # Set and Save API Key
            self.settings.api_key = api_key
            self.settings.save_state()
            self.api_key = api_key

    def load_history(self):
        try:
            self.historian.load_history()
        except (OSError, ValueError, UnicodeError):
            self.request_status.setText('History could not be read; file preserved and saving blocked.')

    def save_history(self):
        try:
            self.historian.save_history()
            return True
        except (OSError, ValueError, UnicodeError):
            self.request_status.setText('History could not be saved; check the data file and permissions.')
            return False

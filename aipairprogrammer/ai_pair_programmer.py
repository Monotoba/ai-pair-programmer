import os

import openai
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QDialog, QComboBox, QLineEdit

from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings
from aipairprogrammer.qt_custom_dialog import CustomDialog
from aipairprogrammer.query_history import QueryHistory


class AIPairProgrammer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = AIPairProgrammerSettings()
        self.api_key = ''
        self.current_model = ''
        self._query_succeeded = False
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
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_query)

        clear_button = QPushButton("Clear Text")
        clear_button.clicked.connect(self.clear_text)

        config_button = QPushButton("Config")
        config_button.clicked.connect(self.show_config_dialog)

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

        button_layout.addWidget(send_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(config_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_model(self, model_name):
        self.current_model = model_name.strip()
        self.settings.model_name = self.current_model
        self.settings.save_state()

    def send_query(self):
        # Add history handling here
        query = self.query_edit.toPlainText()
        if query:
            self._query_succeeded = False
            response_text = self.query_gpt(query)
            if self._query_succeeded:
                self.historian.add(query=query, response=response_text)
                self.historian.save_history()
                self.add_response_text(response_text)
            else:
                self.add_response_text(response_text)
        else:
            self.response_edit.setPlainText("Please enter a query.")

    def query_gpt(self, query) -> str:
        self._query_succeeded = False
        api_key = os.environ.get('OPENAI_API_KEY', '').strip() or self.api_key.strip()
        if not api_key or api_key == '<your api key here>':
            return 'You must set your API key before querying the API.'
        if not self.current_model.strip():
            return 'Enter a model ID available to your OpenAI API account.'
        if not query.strip():
            return 'Please enter a query.'

        try:
            # A per-request client avoids process-global key state and closes
            # its transport even on errors. Do not retry paid requests silently.
            with openai.OpenAI(api_key=api_key, timeout=30.0, max_retries=0,
                               base_url='https://api.openai.com/v1') as client:
                response = client.responses.create(
                    model=self.current_model.strip(),
                    input=query,
                    store=False,
                )
            if response.status == 'incomplete':
                return 'Error: The response was incomplete. Try a shorter request.'
            if response.status != 'completed':
                return 'Error: The API did not complete the response.'
            response_text = response.output_text
            if not response_text or not response_text.strip():
                return 'Error: The API returned no text response.'
            self._query_succeeded = True
            return response_text
        except openai.AuthenticationError:
            return 'Error: Authentication failed. Check your API key.'
        except openai.RateLimitError:
            return 'Error: Rate or quota limit reached. Check your API account.'
        except openai.APITimeoutError:
            return 'Error: The API request timed out. Try again later.'
        except openai.APIConnectionError:
            return 'Error: Could not connect to OpenAI. Check your connection.'
        except openai.APIStatusError:
            return 'Error: The API rejected the request. Check the model ID and account access.'
        except Exception:
            # Provider error bodies may contain prompt content or credentials.
            return 'Error: The request failed unexpectedly.'

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
                              placeholderText=self.api_key,
                              noteText='The key is stored locally in settings.ini as plain text.')
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
        self.historian.load_history()

    def save_history(self):
        self.historian.save_history()

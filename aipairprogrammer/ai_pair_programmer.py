import openai
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QDialog, QComboBox

from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings
from aipairprogrammer.qt_custom_dialog import CustomDialog
from aipairprogrammer.query_history import QueryHistory


class AIPairProgrammer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = AIPairProgrammerSettings()
        self.api_key = ''
        self.current_model = ''
        self.models = {'Davinci': 'davinci',
                       'Curie': 'curie',
                       'Babbage': 'babbage',
                       'Ada': 'ada',
                       'Curie (001)': 'text-curie-001',
                       'Babbage (001)': 'text-babbage-001',
                       'Ada (001)': 'text-ada-001',
                       'Davinci (Text)': 'text-davinci-003',
                       'Davinci (Text/Sm)': 'text-davinci-002',
                       }
        self.model_keys = list(self.models.keys())
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
        self.model_combo_box.addItems(self.models)
        self.model_combo_box.currentIndexChanged.connect(self.update_model)

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

    def update_model(self, index):
        self.current_model = self.models[self.model_keys[index]]
        self.settings.model_name = self.current_model
        self.settings.save_state()

    def send_query(self):
        # Add history handling here
        query = self.query_edit.toPlainText()
        if query:
            response_text = self.query_gpt(query)
            if response_text:
                self.historian.add(query=query, response=response_text)
                self.add_response_text(response_text)
            else:
                self.add_response_text(response_text)
        else:
            self.response_edit.setPlainText("Please enter a query.")

    def query_gpt(self, query) -> str:
        # Code to query OpenAI's API using self.api_key and self.current_model
        # Returns the generated text response
        if self.api_key:
            openai.api_key = self.api_key
        else:
            new_text = 'You must set your API key before querying ChatGPT!'
            self.add_response_text(new_text)

        # Make Query Request
        try:

            response = openai.Completion.create(
                model=self.current_model,
                prompt=query,
                temperature=0.5,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            print(f"Response: {response['choices'][0]['text']}")
            if response.choices:
                response_text = response.choices[0]['text']
                return response_text
            else:
                return "Error"
        except Exception as e:
            return "Error: " + e.__str__()

    def add_response_text(self, new_text: str = ''):
        curr_text = self.response_edit.toPlainText()
        print(f"Current text: {curr_text}")
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
        dialog = CustomDialog(title='Custom Dialog',
                              prompt='Enter some text:',
                              placeholderText=self.api_key,
                              noteText='You can get an api key at: http://openia.com/signup')  # QInputDialog()
        print(f"API Key: {self.api_key}")
        # dialog.setTextValue('This is a test')
        ok = dialog.exec()
        if ok == QDialog.Accepted:
            api_key = dialog.input_field.text()
            # Set and Save API Key
            self.settings.api_key = api_key
            self.settings.save_state()
            self.api_key = api_key

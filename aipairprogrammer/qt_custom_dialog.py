import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout


class CustomDialog(QDialog):
    textEntered = pyqtSignal(str)
    dialogClosed = pyqtSignal()

    def __init__(self, title='', prompt='', placeholderText='', noteText='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        # Create a QLabel widget to display the prompt text
        prompt_label = QLabel(prompt, self)

        font = QFont()
        font.setPointSize(10)
        note_label = QLabel(noteText, self)
        note_label.setFont(font)

        # Create a QLineEdit widget with some initial text
        self.input_field = QLineEdit(placeholderText, self)

        # Create a QPushButton to close the dialog and return the text
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)

        # Create a QPushButton to close the dialog without returning any text
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)

        # Create the QHBoxLayout layout manager for the button row
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)

        # Create the QVBoxLayout layout manager and add the widgets to it
        layout = QVBoxLayout()
        layout.addWidget(prompt_label)
        layout.addWidget(self.input_field)
        layout.addWidget(note_label)
        layout.addLayout(button_layout)

        # Set the layout for the dialog
        self.setLayout(layout)

    # def accept(self):
    #     self.textEntered.emit(self.input_field.text())
    #     super().accept()
    #
    # def reject(self):
    #     self.dialogClosed.emit()
    #     super().reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create an instance of the custom dialog with a window title, prompt text, and initial text
    dialog = CustomDialog(title='Custom Dialog',
                          prompt='Enter some text:',
                          placeholderText='Initial text',
                          noteText='You can get an api key at: http://openia.com/signup')

    # Connect the custom signal to a slot that prints the entered text
    dialog.textEntered.connect(lambda text: print(f'Text entered: {text}'))

    # Connect the custom signal to a slot that handles the case where the user cancels the dialog
    dialog.dialogClosed.connect(lambda: print('Dialog closed without entering text'))

    # Show the dialog
    result = dialog.exec_()

    # Check the result of the dialog and print the text if the 'OK' button was clicked
    if result == QDialog.Accepted:
        print(f'Text entered: {dialog.input_field.text()}')

    sys.exit(app.exec_())

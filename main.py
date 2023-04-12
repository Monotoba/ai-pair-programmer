import sys

from PyQt5.QtWidgets import QApplication

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = AIPairProgrammer()
    widget.load_history()
    widget.show()
    widget.save_history()
    sys.exit(app.exec_())

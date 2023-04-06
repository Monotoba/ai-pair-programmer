import sys

from PyQt5.QtWidgets import QApplication

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = AIPairProgrammer()
    widget.show()
    sys.exit(app.exec_())

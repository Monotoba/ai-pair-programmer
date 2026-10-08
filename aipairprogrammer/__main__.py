import sys

from PyQt5.QtWidgets import QApplication

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer


def main():
    app = QApplication(sys.argv)
    widget = AIPairProgrammer()
    widget.load_history()
    widget.show()
    app.aboutToQuit.connect(widget.save_history)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())

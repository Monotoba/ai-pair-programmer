from aipairprogrammer import __main__ as launcher


def test_launcher_saves_at_shutdown(monkeypatch):
    events = []
    class Signal:
        def connect(self, callback):
            self.callback = callback
    class App:
        def __init__(self, argv):
            self.aboutToQuit = Signal()
        def exec_(self):
            events.append('event loop')
            self.aboutToQuit.callback()
            return 0
    class Widget:
        def load_history(self):
            events.append('load')
        def show(self):
            events.append('show')
        def save_history(self):
            events.append('save')
    monkeypatch.setattr(launcher, 'QApplication', App)
    monkeypatch.setattr(launcher, 'AIPairProgrammer', Widget)
    assert launcher.main() == 0
    assert events == ['load', 'show', 'event loop', 'save']

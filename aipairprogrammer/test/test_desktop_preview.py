import importlib.util
import os
from pathlib import Path

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QDialog, QLineEdit

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer
from aipairprogrammer.qt_custom_dialog import CustomDialog


def test_dialog_hint_is_not_submitted(qtbot):
    dialog = CustomDialog(placeholderText='Session API key')
    qtbot.addWidget(dialog)
    assert dialog.input_field.text() == ''
    assert dialog.input_field.placeholderText() == 'Session API key'
    dialog.accept()
    assert dialog.result() == QDialog.Accepted
    assert dialog.input_field.text() == ''


def test_config_session_key_not_saved(qtbot, monkeypatch):
    widget = AIPairProgrammer()
    qtbot.addWidget(widget)
    seen = []
    class Dialog(CustomDialog):
        def exec(self):
            assert self.input_field.echoMode() == QLineEdit.Password
            seen.append(self.input_field.text())
            self.input_field.setText('private-session-key')
            return QDialog.Accepted
    monkeypatch.setattr('aipairprogrammer.ai_pair_programmer.CustomDialog', Dialog)
    widget.show_config_dialog()
    assert seen == ['']
    assert widget.api_key == 'private-session-key'
    assert 'private-session-key' not in Path(widget.settings.filename).read_text()
    restarted = AIPairProgrammer()
    qtbot.addWidget(restarted)
    assert restarted.api_key == ''
    assert restarted.windowTitle() == 'AI Pair Programmer'


def test_preview_isolated_and_makes_no_api_call(qapp, tmp_path, monkeypatch):
    path = Path(__file__).resolve().parents[2] / 'scripts' / 'preview.py'
    spec = importlib.util.spec_from_file_location('desktop_preview', path)
    preview = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preview)
    def forbidden(*args, **kwargs):
        raise AssertionError('Preview must never call OpenAI')
    monkeypatch.setattr('openai.OpenAI', forbidden)
    old_directory = os.environ['AIPAIRPROGRAMMER_DATA_DIR']
    original = tmp_path / 'app-data' / 'settings.ini'
    original.parent.mkdir(exist_ok=True)
    original.write_text('real settings sentinel')
    output = tmp_path / 'preview.png'
    preview.render_preview(output)
    assert os.environ['AIPAIRPROGRAMMER_DATA_DIR'] == old_directory
    assert original.read_text() == 'real settings sentinel'
    image = QImage(str(output))
    assert not image.isNull()
    assert image.width() >= 760 and image.height() >= 560

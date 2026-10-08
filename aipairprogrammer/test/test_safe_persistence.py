import json
import pickle
from pathlib import Path

import pytest

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer
from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings
from aipairprogrammer.query_history import QueryHistory
from aipairprogrammer.persistence import data_directory


@pytest.mark.parametrize('payload', [
    {}, {'version': 2, 'items': []}, {'version': True, 'items': []},
    {'version': 1, 'items': [{}]},
    {'version': 1, 'items': [{'date': '', 'query': 1, 'response': ''}]},
])
def test_invalid_history_is_preserved(tmp_path, payload):
    path = tmp_path / 'history.json'
    original = json.dumps(payload)
    path.write_text(original)
    history = QueryHistory(path)
    with pytest.raises(ValueError):
        history.load_history()
    with pytest.raises(ValueError):
        history.save_history()
    assert path.read_text() == original


def test_pickle_is_never_executed(tmp_path):
    marker = tmp_path / 'executed'
    class Dangerous:
        def __reduce__(self):
            return (eval, (f"__import__('pathlib').Path({str(marker)!r}).touch()",))
    path = tmp_path / 'history.json'
    original = pickle.dumps(Dangerous())
    path.write_bytes(original)
    history = QueryHistory(path)
    with pytest.raises((ValueError, UnicodeError)):
        history.load_history()
    assert not marker.exists()
    assert path.read_bytes() == original


def test_defaults_leave_legacy_files_untouched(tmp_path):
    old_settings = tmp_path / 'settings.ini'
    old_settings.write_text('[api]\nkey = legacy-key\n[model]\nname = legacy-model\n')
    old_history = tmp_path / 'history.dat'
    old_history.write_bytes(b'legacy history')
    settings = AIPairProgrammerSettings()
    settings.load_state()
    history = QueryHistory()
    history.load_history()
    assert settings.api_key == ''
    assert settings.model_name == ''
    assert history.count() == 0
    assert Path(settings.filename).parent == data_directory()
    assert old_settings.read_text().startswith('[api]')
    assert old_history.read_bytes() == b'legacy history'


def test_explicit_legacy_settings_preserve_model_without_using_key(tmp_path):
    path = tmp_path / 'legacy.ini'
    path.write_text('[api]\nkey = percent%secret\n[model]\nname = old-model\n')
    settings = AIPairProgrammerSettings(path)
    settings.load_state()
    assert settings.api_key == ''
    assert settings.model_name == 'old-model'
    settings.api_key = 'session-key'
    settings.save_state()
    assert 'secret' not in path.read_text()
    assert 'session-key' not in path.read_text()
    assert settings.api_key == 'session-key'


def test_corrupt_history_gui_survives_and_preserves_file(qtbot):
    widget = AIPairProgrammer()
    qtbot.addWidget(widget)
    path = Path(widget.historian.history_filename)
    path.write_text('broken JSON')
    widget.load_history()
    assert 'saving blocked' in widget.request_status.text()
    assert not widget.save_history()
    assert path.read_text() == 'broken JSON'


def test_atomic_failure_preserves_previous_history(tmp_path, monkeypatch):
    history = QueryHistory(tmp_path / 'history.json')
    history.add('first', 'answer')
    history.save_history()
    original = Path(history.history_filename).read_bytes()
    history.add('second', 'answer')
    def fail(*args):
        raise OSError('replacement failed')
    monkeypatch.setattr('aipairprogrammer.persistence.os.replace', fail)
    with pytest.raises(OSError):
        history.save_history()
    assert Path(history.history_filename).read_bytes() == original
    assert list(tmp_path.iterdir()) == [Path(history.history_filename)]

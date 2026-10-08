import threading

import pytest
from PyQt5.QtCore import QTimer

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer


@pytest.fixture()
def pending_request(qtbot, monkeypatch):
    app = AIPairProgrammer()
    qtbot.addWidget(app)
    app.api_key = 'offline-key'
    app.current_model = 'offline-model'
    app.query_edit.setPlainText('Original question')
    started = threading.Event()
    release = threading.Event()
    calls = []
    def blocked(query, model, key):
        calls.append((query, model, key, threading.get_ident()))
        started.set()
        release.wait(5)
        return 'Worker answer', True
    monkeypatch.setattr('aipairprogrammer.ai_pair_programmer.execute_query', blocked)
    yield app, started, release, calls
    release.set()
    qtbot.waitUntil(lambda: app._request is None, timeout=6000)


def test_request_keeps_gui_event_loop_responsive(pending_request, qtbot):
    app, started, release, calls = pending_request
    app.send_query()
    qtbot.waitUntil(started.is_set)
    ticks = []
    QTimer.singleShot(0, lambda: ticks.append('GUI tick'))
    qtbot.waitUntil(lambda: bool(ticks))
    assert calls[0][3] != threading.get_ident()
    assert not app.send_button.isEnabled()
    assert app.cancel_button.isEnabled()
    app.query_edit.setPlainText('Edited while waiting')
    release.set()
    qtbot.waitUntil(lambda: app._request is None)
    assert app.historian.last().query == 'Original question'
    assert app.historian.last().response == 'Worker answer'
    assert app.send_button.isEnabled()
    assert not app.cancel_button.isEnabled()
    assert app.model_combo_box.isEnabled()


def test_duplicate_submission_is_ignored(pending_request, qtbot):
    app, started, release, calls = pending_request
    app.send_query()
    qtbot.waitUntil(started.is_set)
    app.send_query()
    assert len(calls) == 1
    release.set()
    qtbot.waitUntil(lambda: app._request is None)
    assert app.historian.count() == 1


def test_cancel_discards_result_and_waits_before_resubmission(pending_request, qtbot):
    app, started, release, calls = pending_request
    app.send_query()
    qtbot.waitUntil(started.is_set)
    app.cancel_request()
    assert app._request.isInterruptionRequested()
    assert not app.send_button.isEnabled()
    assert not app.cancel_button.isEnabled()
    app._receive_result('Already queued response', True)
    app.send_query()
    assert len(calls) == 1
    release.set()
    qtbot.waitUntil(lambda: app._request is None)
    assert app.historian.count() == 0
    assert app.response_edit.toPlainText() == ''
    assert app.request_status.text() == 'Request cancelled locally'
    assert app.send_button.isEnabled()


def test_close_during_request_waits_for_thread(pending_request, qtbot):
    app, started, release, _ = pending_request
    app.show()
    app.send_query()
    qtbot.waitUntil(started.is_set)
    app.close()
    assert app.isVisible()
    assert app._close_when_finished
    release.set()
    qtbot.waitUntil(lambda: app._request is None)
    qtbot.waitUntil(lambda: not app.isVisible())
    assert app.historian.count() == 0


def test_invalid_request_never_starts_worker(pending_request):
    app, started, _, calls = pending_request
    app.current_model = ''
    app.send_query()
    assert app._request is None
    assert not started.is_set()
    assert not calls
    assert 'Enter a model ID' in app.response_edit.toPlainText()


def test_worker_exception_is_sanitized(pending_request, qtbot, monkeypatch):
    app, _, _, _ = pending_request
    def fail(*args):
        raise RuntimeError('private credential')
    monkeypatch.setattr('aipairprogrammer.ai_pair_programmer.execute_query', fail)
    app.send_query()
    qtbot.waitUntil(lambda: app._request is None)
    assert 'failed unexpectedly' in app.response_edit.toPlainText()
    assert 'private' not in app.response_edit.toPlainText()
    assert app.historian.count() == 0
    assert app.send_button.isEnabled()

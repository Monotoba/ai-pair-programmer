#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: This test file is used to test the AIPairProgrammer class
# and not it's PyQT5 GUI. The GUI tests can be found in test_app.py.
import pytest
from datetime import datetime

from aipairprogrammer.ai_pair_programmer import AIPairProgrammer


@pytest.fixture()
def app(qtbot):
    app = AIPairProgrammer()
    qtbot.addWidget(app)
    return app


def test_update_model(app):
    # Current model defaults to davinci
    app.update_model(index=0)
    assert app.current_model == app.models[app.model_keys[0]]
    # Update to Curie model
    app.update_model(index=1)
    assert app.current_model == app.models[app.model_keys[1]]
    # Set it back to davinci
    app.update_model(index=0)
    assert app.current_model == app.models[app.model_keys[0]]

def test_query_gpt(app, monkeypatch):
    calls = []
    def complete(**kwargs):
        calls.append(kwargs)
        from types import SimpleNamespace
        return SimpleNamespace(choices=[{'text': 'Mocked answer'}])
    monkeypatch.setattr('openai.Completion.create', complete)
    app.api_key = 'test-key'
    assert app.query_gpt('Question') == 'Mocked answer'
    assert calls[0]['prompt'] == 'Question'
    assert calls[0]['model'] == app.current_model


@pytest.mark.parametrize('key', ['', '<your api key here>'])
def test_missing_key_never_calls_api(app, monkeypatch, key):
    def unexpected(**kwargs):
        pytest.fail('API called without a configured key')
    monkeypatch.setattr('openai.Completion.create', unexpected)
    app.api_key = key
    assert 'set your API key' in app.query_gpt('Question')


def test_api_failure_is_displayable(app, monkeypatch):
    def fail(**kwargs):
        raise RuntimeError('Mock API failure')
    monkeypatch.setattr('openai.Completion.create', fail)
    app.api_key = 'test-key'
    assert app.query_gpt('Question') == 'Error: Mock API failure'


def test_send_query_saves_response(app, monkeypatch):
    monkeypatch.setattr(app, 'query_gpt', lambda query: 'Answer')
    app.query_edit.setPlainText('Question')
    app.send_query()
    assert app.historian.last().query == 'Question'
    assert app.historian.last().response == 'Answer'
    assert 'Answer' in app.response_edit.toPlainText()


def test_response_text_is_not_logged(app, capsys):
    app.add_response_text('private test response')
    assert capsys.readouterr().out == ''


def test_config_masks_key_and_does_not_log_it(app, monkeypatch, capsys):
    from PyQt5.QtWidgets import QDialog, QLineEdit
    modes = []
    class Field:
        def setEchoMode(self, mode):
            modes.append(mode)
    class Dialog:
        input_field = Field()
        def __init__(self, **kwargs):
            assert kwargs['placeholderText'] == 'private-test-key'
        def exec(self):
            return QDialog.Rejected
    app.api_key = 'private-test-key'
    monkeypatch.setattr('aipairprogrammer.ai_pair_programmer.CustomDialog', Dialog)
    app.show_config_dialog()
    assert modes == [QLineEdit.Password]
    assert capsys.readouterr().out == ''

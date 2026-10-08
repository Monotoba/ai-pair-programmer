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
    app.model_combo_box.setCurrentText('account-model')
    assert app.current_model == 'account-model'
    assert app.settings.model_name == 'account-model'


def test_saved_model_is_restored(app, qtbot):
    app.model_combo_box.setCurrentText('saved-model')
    restored = AIPairProgrammer()
    qtbot.addWidget(restored)
    assert restored.current_model == 'saved-model'
    assert restored.model_combo_box.currentText() == 'saved-model'


@pytest.fixture()
def api(app, monkeypatch):
    from types import SimpleNamespace
    calls = []
    response = SimpleNamespace(status='completed', output_text='Mocked answer')
    class Client:
        def __init__(self, **kwargs):
            self.responses = self
            calls.append(('client', kwargs))
        def __enter__(self):
            return self
        def __exit__(self, *args):
            calls.append(('closed', None))
        def create(self, **kwargs):
            calls.append(('request', kwargs))
            return response
    monkeypatch.setattr('openai.OpenAI', Client)
    app.api_key = 'test-key'
    app.model_combo_box.setCurrentText('test-model')
    return calls, response


def test_query_gpt(app, api):
    calls, _ = api
    assert app.query_gpt('Question') == 'Mocked answer'
    assert calls == [
        ('client', {'api_key': 'test-key', 'timeout': 30.0, 'max_retries': 0,
                    'base_url': 'https://api.openai.com/v1'}),
        ('request', {'model': 'test-model', 'input': 'Question', 'store': False}),
        ('closed', None),
    ]
    assert app._query_succeeded


@pytest.mark.parametrize('key', ['', '<your api key here>'])
def test_missing_key_never_calls_api(app, monkeypatch, key):
    def unexpected(**kwargs):
        pytest.fail('API called without a configured key')
    monkeypatch.setattr('openai.OpenAI', unexpected)
    app.api_key = key
    assert 'set your API key' in app.query_gpt('Question')
    assert not app._query_succeeded


def test_environment_key_is_used_without_persistence(app, api, monkeypatch):
    calls, _ = api
    monkeypatch.setenv('OPENAI_API_KEY', 'environment-test-key')
    assert app.query_gpt('Question') == 'Mocked answer'
    assert calls[0][1]['api_key'] == 'environment-test-key'
    assert app.settings.api_key != 'environment-test-key'
    from pathlib import Path
    assert 'environment-test-key' not in Path(app.settings.filename).read_text()


@pytest.mark.parametrize('query, model, expected', [
    ('Question', '', 'Enter a model ID'),
    (' ', 'test-model', 'Please enter a query'),
])
def test_validation_never_calls_api(app, api, query, model, expected):
    calls, _ = api
    app.current_model = model
    assert expected in app.query_gpt(query)
    assert calls == []


@pytest.mark.parametrize('status, text', [
    ('completed', ''), ('completed', '  '), ('incomplete', 'partial'),
    ('failed', 'partial'),
])
def test_unusable_response_is_not_saved(app, api, status, text, qtbot):
    _, response = api
    response.status = status
    response.output_text = text
    app.query_edit.setPlainText('Question')
    app.send_query()
    qtbot.waitUntil(lambda: app._request is None)
    assert app.response_edit.toPlainText().startswith('Error:')
    assert app.historian.count() == 0


def test_api_failure_is_displayable(app, monkeypatch, qtbot):
    def fail(**kwargs):
        raise RuntimeError('private-test-key private prompt')
    monkeypatch.setattr('openai.OpenAI', fail)
    app.api_key = 'private-test-key'
    app.current_model = 'test-model'
    app.query_edit.setPlainText('Question')
    app.send_query()
    qtbot.waitUntil(lambda: app._request is None)
    assert 'Error: The request failed unexpectedly.' in app.response_edit.toPlainText()
    assert 'private' not in app.response_edit.toPlainText()
    assert app.historian.count() == 0


def test_send_query_saves_response(app, api, qtbot):
    app.query_edit.setPlainText('Question')
    app.send_query()
    qtbot.waitUntil(lambda: app._request is None)
    assert app.historian.last().query == 'Question'
    assert app.historian.last().response == 'Mocked answer'
    assert 'Mocked answer' in app.response_edit.toPlainText()


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
            assert kwargs['placeholderText'] == 'Session API key'
            assert 'private-test-key' not in str(kwargs)
        def exec(self):
            return QDialog.Rejected
    app.api_key = 'private-test-key'
    monkeypatch.setattr('aipairprogrammer.ai_pair_programmer.CustomDialog', Dialog)
    app.show_config_dialog()
    assert modes == [QLineEdit.Password]
    assert capsys.readouterr().out == ''


@pytest.mark.parametrize('kind, expected', [
    ('auth', 'Authentication failed'), ('rate', 'Rate or quota limit'),
    ('timeout', 'timed out'), ('connection', 'Could not connect'),
    ('status', 'API rejected'),
])
def test_sdk_errors_are_sanitized(app, monkeypatch, kind, expected):
    import httpx
    import openai
    request = httpx.Request('POST', 'https://api.openai.com/v1/responses')
    response = httpx.Response(400, request=request)
    if kind == 'auth':
        error = openai.AuthenticationError('private body', response=response, body=None)
    elif kind == 'rate':
        error = openai.RateLimitError('private body', response=response, body=None)
    elif kind == 'timeout':
        error = openai.APITimeoutError(request=request)
    elif kind == 'connection':
        error = openai.APIConnectionError(request=request)
    else:
        error = openai.APIStatusError('private body', response=response, body=None)
    def fail(**kwargs):
        raise error
    monkeypatch.setattr('openai.OpenAI', fail)
    app.api_key = 'test-key'
    app.current_model = 'test-model'
    result = app.query_gpt('Question')
    assert expected in result
    assert 'private body' not in result
    assert not app._query_succeeded


def test_responses_sdk_serialization_offline(app, monkeypatch):
    import json
    import httpx
    import openai
    requests = []
    def respond(request):
        requests.append(request)
        return httpx.Response(200, json={
            'id': 'resp_test', 'object': 'response', 'created_at': 1,
            'model': 'test-model', 'status': 'completed', 'error': None,
            'incomplete_details': None,
            'output': [{'type': 'message', 'id': 'msg_test',
                        'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': 'SDK answer',
                                     'annotations': []}]}],
        })
    original = openai.OpenAI
    def client(**kwargs):
        return original(**kwargs, http_client=httpx.Client(
            transport=httpx.MockTransport(respond)))
    monkeypatch.setattr('openai.OpenAI', client)
    app.api_key = 'offline-test-key'
    app.current_model = 'test-model'
    assert app.query_gpt('SDK question') == 'SDK answer'
    assert len(requests) == 1
    assert str(requests[0].url) == 'https://api.openai.com/v1/responses'
    body = json.loads(requests[0].content)
    assert body['model'] == 'test-model'
    assert body['input'] == 'SDK question'
    assert body['store'] is False
    assert app._query_succeeded

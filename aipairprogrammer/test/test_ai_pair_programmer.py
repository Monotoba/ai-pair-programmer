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

def test_query_gpt(app):
    # Get our testing api key
    app.settings.filename = '../../.secret/settings.ini'
    app.settings.loadState()
    app.api_key = app.settings.get_api_key()
    # Now we can make the api call
    response_text = app.query_gpt(query="What is today's date in mm-dd-YYYY format?")  # Returned as something like: Today's date is April 7, 2023.
    # Get the current date and format fstring
    current_date = datetime.now()  # We may need to set a timezone?
    month_name = current_date.strftime('%b')
    day_num = current_date.day
    year = current_date.year
    # compare
    assert response_text !=  "Error"

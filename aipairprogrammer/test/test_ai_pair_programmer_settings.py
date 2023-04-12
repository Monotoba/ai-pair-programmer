#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import pytest

from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings


@pytest.fixture()
def settings():
    # Instantiate the settings object for use in tests
    cwd = os.getcwd()
    filename = f"{cwd}/.secret/example_settings.ini"
    settings = AIPairProgrammerSettings(filename=filename)
    return settings


def test_get_state(settings):
    state_ = settings.get_state()
    assert state_ == settings


def test_settings_filename(settings):
    # Manually set settings file name
    cwd = os.getcwd()
    filename = f"{cwd}/.secret/example_settings.ini"
    settings.settings_filename(filename=filename)
    assert settings.filename == filename


def test_load_state(settings):
    # Load state should create a settings.ini
    # file if not exists, and set settings values
    # from file.
    assert settings.api_key == ""
    assert settings.model_name == ""
    # Now load the settings from the example file
    settings.load_state()
    # query changes
    assert settings.api_key == "<your api key here>"
    assert settings.model_name == "davinci"


def test_save_state(settings):
    # Get current settings
    old_api_key = settings.api_key
    old_model_name = settings.model_name
    new_api_key = "sk_5659873451093_4345"
    new_model_name = "curie"
    # set new values
    settings.api_key = new_api_key
    settings.model_name = new_model_name
    assert settings.api_key == new_api_key
    assert settings.model_name == new_model_name
    # Rest value for remaining tests
    settings.api_key = old_api_key
    settings.model_name = old_model_name
    # Confirm settings have been restored
    assert settings.api_key == old_api_key
    assert settings.model_name == old_model_name

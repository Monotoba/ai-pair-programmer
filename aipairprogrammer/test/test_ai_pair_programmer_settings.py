#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from aipairprogrammer.ai_pair_programmer_settings import AIPairProgrammerSettings


@pytest.fixture()
def test_settings():
    settings = AIPairProgrammerSettings()
    return settings

def test_get_state(settings):
    state_ = settings.get_state()
    assert state_ == settings


def test_load_state(settings):
    assert False


def test_save_state(settings):
    assert False


def test_get_api_key(settings):
    assert False


def test_set_api_key(settings):
    assert False


def test_get_model_name(settings):
    assert False

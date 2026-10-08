# AI Pair Programmer

[![Tests](https://github.com/Monotoba/ai-pair-programmer/actions/workflows/tests.yml/badge.svg)](https://github.com/Monotoba/ai-pair-programmer/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)
[![License](https://img.shields.io/badge/license-BSD--2--Clause-blue)](LICENSE.md)

An experimental PyQt5 desktop assistant for asking programming questions,
viewing responses, and browsing local query history.

**Work in progress:** this 2023 prototype uses the legacy OpenAI SDK and
Completion API with a historical model list. Live API functionality has not
been validated. Do not treat this as a ready-to-use coding assistant yet.
The current cleanup establishes installation and offline regression tests.

## What is implemented

- Query and response text panes with model selection.
- Local history with previous/next navigation.
- API-key configuration and saved settings.
- Clear text without deleting history.

## Developer quick start

Requires Python 3.10+ and a graphical desktop. Linux, macOS, and Windows
have an offline CI matrix; automated Qt tests use offscreen rendering.

```sh
git clone https://github.com/Monotoba/ai-pair-programmer.git
cd ai-pair-programmer
python -m venv .venv
```

Activate with `source .venv/bin/activate` on Linux/macOS, or
`.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```sh
python -m pip install -e ".[test]"
python -m aipairprogrammer
```

The installed `ai-pair-programmer` command and `python main.py` also launch
the app. Opening the GUI does not send a request; clicking Send does.

## Data and limitations

Settings and `history.dat` are stored in the working directory. The API key
is stored in **plain text** in `settings.ini`; responses and queries are stored
in history. These files are ignored by Git. Only load your own history file:
the legacy pickle format is unsafe for untrusted files.

Requests run synchronously and may freeze the UI while waiting. History
contains independent queries, not conversational sessions. The model picker
and API integration need modernization before live use. No live API request,
billing, or model availability is exercised by the automated tests.

See the [user guide](docs/USERGUIDE.md), [roadmap](docs/ROADMAP.md), and
[contributor instructions](CONTRIBUTING.md). Specific bug reports and small
pull requests are welcome, especially for the roadmap items.

Licensed under [BSD-2-Clause](LICENSE.md).

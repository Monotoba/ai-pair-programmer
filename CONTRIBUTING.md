# Contributing

Use Python 3.10+ and install `python -m pip install -e ".[test]"`.

Run the offline tests with:

```sh
QT_QPA_PLATFORM=offscreen python -m pytest -q
```

In PowerShell, set `$env:QT_QPA_PLATFORM = "offscreen"` first, then run
`python -m pytest -q`. Tests must mock API calls and use temporary files;
never require real credentials, network requests, or paid API usage.

For packaging checks:

```sh
python -m pip install build
python -m build
python scripts/check_wheel.py
```

Add a regression test for every code change. Keep pull requests focused and
follow the ordered [roadmap](docs/ROADMAP.md). Include reproduction steps,
OS/Python versions, and sanitized error messages in issues; omit keys and
private queries. No PyPI publication is planned in this cleanup.

The safe screenshot script is `scripts/preview.py`. After installing the
checkout, run it with `QT_QPA_PLATFORM=offscreen`; it uses labeled sample text
and isolated temporary settings, without making an API request. Keep preview
claims separate from live/API or native desktop validation.

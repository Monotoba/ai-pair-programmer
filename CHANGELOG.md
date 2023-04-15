# AI Pair Programmer
## Change Log

0.0.7 2023-04-15
- Added test/historytest.txt (test history data file) to .gitignore
- Added tests to test_query_history.py.
- Changed method name of QueryHistory.empty_history() to QueryHistory.clear().

0.0.6 2023-04-12
- Changed test_ai_pair_programmer_settings.py to make use of example_settings.ini more consistent with.
- Added is_in_bounds() and limit() methods to QueryHistory class.
- Changed some method names to match proper python formatting.
- Added history.dat to .gitignore file.
- Updated CHANGELOG.

0.0.5 2023-04-11
- Added .secret directory.
- Added example_settings.ini.
- Added settings.ini to .gitignore file.
- Converted api key and model_name in ai_pair_programmer_settings.py to properties.
- Renamed loadState and saveState in ai_pair_programmer_settings.py to load_state and save_state respectively.

0.0.4 2023-04-07
- Fixed links in README.md file.
- Started adding tests to test_ai_pair_programmer_settings.py file.

0.0.3 2023-04-07
- Added test files to test directory.
- Added pytest-qt as test dependency.

0.0.2 2023-04-04 - Renamed Branch name to main
- Renamed local repo master branch to main. This

0.0.1 2023-04-03 - Initial Release:
- Packaged project for PyPi.
- Added CHANGELOG.md to project.
- Added README.md file to document the project.
- Notes: This is the initial release of AI Pair Programmer. 
A small Python 3.7+ applet that allows the user to send queries
to ChatGPT 3+ and receive a response. The applet has a few simple
features such as the ability for the user to select which ChatGPT
model they query, and a crude history feature. This software is 
simply a standalone version and POC for a PyCharm plugin I am 
working on.



----------------------------------------------------------------
Notes on change log format:
(version) (bullet) Date (YYYY-mm-dd [optional time in hh:mm]) - Short description:
Long description (keep lines at ~65 characters in length). As many 
lines as needed. Place all entries in reverse chronological order 
so the most recent changes are at the top of the file. This format
information will be removed in some future version of this file.

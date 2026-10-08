# AI Pair Programmer user guide

This is a work-in-progress desktop prototype. See the [README](../README.md)
for installation and current limitations. The live OpenAI integration is
legacy and has not been validated for current use.

## Interface

Enter a question in the query pane and press **Send** to request a response.
Sending a request transmits that text to OpenAI when an API key is configured.
Successful responses are appended to the response pane and saved in local
history. **Prev** and **Next** browse saved responses; **Clear Text** clears
the two text panes without removing history.

The model picker currently lists historical Completion models. **Config**
opens the API-key dialog, which masks the key on screen but saves it in plain
text in `settings.ini` in the current directory. The model setting is saved,
but restoring the picker selection is a remaining task.

## Local files

- `settings.ini`: API key and model name.
- `history.dat`: queries, responses, and timestamps in legacy pickle format.

Do not share these files or open a history file supplied by another person.
The app loads history on startup and saves it after responses and on normal
exit. History has no conversation sessions or search yet.

## Development

GUI code is in `aipairprogrammer/ai_pair_programmer.py`, configuration in
`ai_pair_programmer_settings.py`, and persistence in `query_history.py`.
The custom key dialog is in `qt_custom_dialog.py`. Tests use temporary files
and mocked API calls. Follow [CONTRIBUTING](../CONTRIBUTING.md) to run them.

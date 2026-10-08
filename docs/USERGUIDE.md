# AI Pair Programmer user guide

This is a work-in-progress desktop prototype. See the [README](../README.md)
for installation and current limitations. The Responses API integration has offline regression tests; live account
access and billing behavior have not been tested.

## Interface

Enter a question in the query pane and press **Send** to request a response.
Sending a request transmits that text to OpenAI when an API key is configured.
Completed, non-empty text responses are appended to the response pane and saved in local
history. **Prev** and **Next** browse saved responses; **Clear Text** clears
the two text panes without removing history.

The model field accepts a Responses-compatible model ID available to your
API account. The app starts with no model selected unless one was saved.
Saved historical IDs remain visible and must be replaced before use. **Config**
opens the API-key dialog, which masks the key on screen but saves it in plain
text in `settings.ini` in the current directory. The model setting is saved and restored on startup. An `OPENAI_API_KEY`
environment variable takes precedence over a configured key and is never
copied into the settings file. Requests go to the official OpenAI endpoint.

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

## Errors and request limits

Missing keys, blank models, and blank questions are rejected locally. API
failures show brief messages for authentication, quota/rate limits, timeouts,
connection problems, and rejected requests. Provider error bodies are not
displayed. Errors and incomplete/empty responses are not saved in history.

The SDK uses a 30-second timeout and no automatic retries. Requests currently
block the GUI thread; see the [roadmap](ROADMAP.md) for the next step. Sending
queries may incur API charges. `store=False` disables response storage for
this request but is not a promise of zero provider retention.

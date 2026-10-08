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
opens the API-key dialog, which masks the key on screen and keeps it in memory
for the current session only. The model setting is saved and restored on startup. An `OPENAI_API_KEY`
environment variable takes precedence over a configured key and is never
copied into the settings file. Requests go to the official OpenAI endpoint.

## Local files

- `settings.ini`: model name only; API keys are never saved by this version.
- `history.json`: validated version-1 JSON containing queries, responses, and timestamps.

Default directory:

| Platform | Directory |
| --- | --- |
| Linux | `$XDG_DATA_HOME/ai-pair-programmer`, or `~/.local/share/ai-pair-programmer` |
| macOS | `~/Library/Application Support/ai-pair-programmer` |
| Windows | `%LOCALAPPDATA%\ai-pair-programmer` |

Set `AIPAIRPROGRAMMER_DATA_DIR` to override the directory. Avoid shared folders.
On Unix, new files use owner-only permissions and newly created data directories
use owner-only access. Windows access follows the directory's ACLs.
Do not share history: it contains your questions and responses.
The app loads history on startup and saves it after responses and on normal
exit. Writes replace the destination atomically. A read failure blocks saving
to preserve the original file; move it aside or repair it, then restart.
History has no conversation sessions or search yet.

## Upgrading from legacy storage

The old working-directory `settings.ini` and `history.dat` are left untouched.
They are not loaded automatically. Re-enter your model ID and configure
`OPENAI_API_KEY` or enter a session key in **Config**. The old settings file may
still contain a plaintext key; remove that key yourself once you have moved it
to your chosen configuration method. No backup containing the key is created.

Pickle history is no longer loaded, including when supplied as a custom path.
There is no automatic pickle converter in this version because loading pickle
can execute code. Keep your old file if you need its contents; do not unpickle
files from other people. You can manually copy existing text into the following
JSON structure in the new data directory, with the app closed:

```json
{
  "version": 1,
  "items": [
    {"date": "2026-10-08 12:00:00", "query": "Your question", "response": "Your answer"}
  ]
}
```

All three item fields must be strings. Invalid JSON, unknown versions, and
invalid items produce a history error without overwriting the file. Keep a
copy of existing JSON before editing it.

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

The SDK uses a 30-second timeout and no automatic retries. Requests run in a
worker thread. **Send**, model configuration, and key configuration stay
disabled while the request runs; query editing, history navigation, and
Clear Text remain available. The query/model/key are captured at submission.

**Cancel request** discards the eventual response locally. It does not abort
provider-side processing or guarantee that charges are avoided. Send remains
disabled until the worker finishes. Closing the window during a request
cancels locally and defers closing until the worker exits safely. The SDK
timeout bounds individual network waits, not an absolute total runtime. Sending
queries may incur API charges. `store=False` disables response storage for
this request but is not a promise of zero provider retention.

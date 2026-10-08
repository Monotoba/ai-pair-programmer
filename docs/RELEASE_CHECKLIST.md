# 0.1.0a1 experimental alpha

Published on 2026-10-08 as a [GitHub prerelease](https://github.com/Monotoba/ai-pair-programmer/releases/tag/v0.1.0a1).
PyPI publication remains out of scope.

## Completed offline checks

- 63 regression tests covering settings, JSON history, worker behavior,
  API mocks, launcher shutdown, key dialog, and isolated preview rendering.
- Real Qt widget rendered offscreen; README screenshot uses labeled sample data.
- Wheel and source distribution built; wheel installed and started outside
  the checkout, with a history round trip in an isolated temporary directory.
- All six candidate PR and post-merge CI jobs passed, covering Python 3.10/3.12
  on Linux, Windows, and macOS.
- BSD-2-Clause license, build/language/GUI/status badges, contribution guide,
  upgrade notes, troubleshooting, and roadmap included.

- GitHub prerelease published with wheel, source archive, and SHA-256 checksums;
  uploaded package digests matched the local checksums.

## Outstanding validation

- Native interactive desktop launch, display scaling, and keyboard behavior
  on supported operating systems. Offscreen CI does not cover native plugins.
- A small live request using an explicitly configured test account and model,
  followed by checking response rendering and saved history. No live request
  has been made; API access, model availability, and billing remain unverified.


A release must be marked as a prerelease and clearly state the outstanding
validation. Do not present the candidate as production-ready or live-validated.

## Alpha release summary

Experimental PyQt5 programming assistant with the OpenAI Responses API,
editable model IDs, responsive background requests, and local cancellation.
Settings/history use per-user storage and atomic writes; API keys entered in
Config remain in memory for one session. History uses validated JSON.

Legacy working-directory settings and pickle history are left untouched and
not imported automatically. Re-enter the model and configure an environment
or session key. See the user guide before upgrading.

Validated with offline regression tests and installed-wheel/offscreen Qt
checks. Live API/account/billing and native interactive desktop behavior have
not been validated. Cancellation does not guarantee stopped provider work or
avoided charges. This is an alpha for testing and feedback.

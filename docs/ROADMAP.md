# Work toward an initial alpha

Complete in this order:

1. **Offline baseline:** repair packaging, isolate tests, add CI, and fix
   missing-history startup and configured history paths. Implemented in this
   cleanup; CI must pass before merge.
2. **Current API integration:** replace the legacy Completion call and SDK,
   support a configurable model, restore the selected model on startup,
   handle empty responses and provider errors, and verify request/response
   behavior with mocks. Validate any live request separately with an explicitly
   configured test account.
3. **Responsive UI:** run requests off the GUI thread, prevent duplicate
   submissions, and implement timeouts/cancellation with GUI tests.
4. **Persistence:** migrate pickle history to a validated JSON format, choose
   a per-user data directory, and store API keys in an OS credential store or
   accept an environment variable without writing the key to disk. Plan
   compatibility with existing local files explicitly.
5. **Alpha readiness:** perform desktop smoke tests, add a screenshot and
   troubleshooting notes, build and install the release wheel outside the
   checkout, and publish an alpha only after these checks are complete.

Session history, multiple providers, themes, and accessibility remain later
improvements. The current cleanup is not an API modernization or a release.

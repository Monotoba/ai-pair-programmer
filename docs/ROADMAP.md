# Work toward an initial alpha

Complete in this order:

1. **Offline baseline:** repair packaging, isolate tests, add CI, and fix
   missing-history startup and configured history paths. Implemented in this
   cleanup; all six CI jobs passed before merge.
2. **Current API integration:** implemented the Responses API, configurable
   model ID with startup restoration, sanitized errors, and empty/incomplete
   response handling with mocks. Environment keys are supported without
   copying them into settings. Live validation remains pending and requires
   an explicitly configured test account.
3. **Responsive UI:** implemented worker-thread requests, submission snapshots,
   duplicate prevention, local result cancellation, and safe deferred closing
   with GUI regression tests. The SDK timeout remains in place; cancellation
   does not guarantee that provider processing or billing stops.
4. **Persistence:** implemented validated JSON history, atomic writes,
   per-user paths, session-only keys, and preservation of unreadable files.
   Legacy files stay untouched and require explicit reconfiguration; automatic
   pickle conversion is intentionally unavailable. Regression tests cover
   invalid data, executable pickle rejection, write failures, and legacy files.
5. **Alpha readiness:** `0.1.0a1` published as an experimental GitHub prerelease with an actual offscreen Qt
   preview, troubleshooting notes, regression tests, and an installed-wheel
   smoke test outside the checkout. Interactive desktop and live-account
   validation remain pending. See [release checks](RELEASE_CHECKLIST.md); an
   alpha must clearly disclose these limits.

Session history, multiple providers, themes, and accessibility remain later
improvements. The alpha is available for testing; live API and native desktop
validation remain outstanding.

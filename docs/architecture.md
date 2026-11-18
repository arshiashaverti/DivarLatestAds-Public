# Architecture

## Overview

The application is organized as a small Python package with separate modules.

## Components

- `config.py`: environment-based settings and Telegram credential validation.
- `scraper.py`: browser navigation and listing extraction.
- `storage.py`: JSON state loading, atomic state saving, and new-ID comparison.
- `telegram.py`: Telegram Bot API message delivery.
- `local_monitor.py`: repeated local checks and Windows desktop notifications.
- `cloud_monitor.py`: one cloud check and Telegram notifications.
- `__main__.py`: command-line listing export.

## Data flow

1. Load runtime configuration.
2. Open the configured search page with Playwright.
3. Extract listing IDs, titles, and URLs.
4. Load previously stored IDs.
5. Compare current IDs with known IDs.
6. Notify about newly detected listings when applicable.
7. Persist updated state.

## Persistence

The default state path is `data/known_ads.json`. Runtime data is excluded from Git.

State writes use a temporary file followed by `os.replace` to reduce the risk of partially written JSON files.

## Security

- Telegram credentials are read from environment variables.
- No real credentials are included in the repository.
- Local state and generated data are excluded by `.gitignore`.
- CI workflows use read-only repository permissions.

## Known limitations

- The scraper depends on the target website's page structure.
- The current test suite uses unit tests and does not validate live website behavior.
- Cloud state persistence must be configured by the deployment environment.
- The local monitor is a foreground process, not a Windows service.
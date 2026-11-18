# Development History

## Project origin

The project began as a small Python automation tool for monitoring a focused Divar search page.

## Initial implementation

The first version used separate scripts for:
- Listing export.
- Local Windows monitoring.
- Cloud monitoring with Telegram notifications.

The scripts used Playwright to open the search page and JSON files to remember previously seen listing IDs.

## Refactoring

The public portfolio edition reorganizes the code into a Python package:
- Shared scraping logic.
- Centralized configuration.
- Separate storage and notification modules.
- Explicit command entry points.
- Unit tests.
- Documentation and CI checks.

## Publication goals

The public edition is intended to demonstrate practical Python development, browser automation, API integration, modular design, testing, and version control.

The public repository does not include the original runtime data, credentials, or private Git history.
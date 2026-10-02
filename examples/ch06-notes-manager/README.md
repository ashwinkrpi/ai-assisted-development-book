# Notes Manager

A simple command-line notes manager with local JSON persistence.

## Install

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

## Usage

    notes add "Title" "Body text"
    notes list
    notes search "keyword"
    notes edit <id-prefix> --title "New title" --body "New body"
    notes delete <id-prefix>

Notes are stored in `~/.notes-manager/notes.json`. Use `--storage <file>`
before the command to use a different file.

## Development

    python3 -m pytest

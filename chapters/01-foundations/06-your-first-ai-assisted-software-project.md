# Chapter 6 — Your First AI-Assisted Software Project

> *The fastest way to learn AI-assisted development is to build a complete project using disciplined engineering practices from the very beginning — not after the first time something breaks.*

## Learning Objectives

By the end of this chapter, you will be able to:

- Apply the full AI-assisted workflow from Chapters 1–5 to a real, working project.
- Build a small application incrementally, with each step independently reviewable.
- Validate AI-generated work with a real test suite, not just a visual check.
- Document and test continuously, producing artifacts a reviewer — or another engineer — could pick up cold.

---

## Project Overview

You'll build a command-line **Notes Manager**: a small application supporting create, edit, delete, search, and persistent local storage. It's deliberately simple — the point of this chapter isn't the notes app, it's practicing the complete workflow end to end on something small enough to hold in your head at once.

### Requirements

**Functional:**
- Create, read, edit, and delete notes (CRUD)
- Search notes by title or body content
- Persist notes locally between runs

**Non-functional:**
- Cross-platform (pure Python standard library — no OS-specific dependencies)
- Maintainable (clear separation between storage, business logic, and CLI)
- Testable (business logic isolated from I/O so it can be tested without touching the filesystem in awkward ways)

### Architecture

```mermaid
flowchart LR
CLI[CLI Layer] --> Service[Service Layer]
Service --> Repository[Repository Layer]
Repository --> Storage[(JSON File)]
```

This is a deliberately layered design, and the layering is doing real work, not just adding files for the sake of structure:

- **Repository** — the only layer that knows storage is a JSON file. If you swapped it for SQLite later, nothing above it would change.
- **Service** — business rules (a note must have a non-empty title, editing updates a timestamp) live here, independent of both storage and the CLI.
- **CLI** — parses arguments and formats output; it has no business logic of its own.

This separation is also what makes the test suite in Section 6.5 possible without spinning up a subprocess for every test — the service layer can be tested directly.

---

## 6.1 Step 1 — Project Structure

```bash
mkdir -p notes-manager/src/notes_manager notes-manager/tests
cd notes-manager
touch src/notes_manager/__init__.py
git init
```

```text
notes-manager/
├── src/
│   └── notes_manager/
│       ├── __init__.py
│       ├── models.py
│       ├── repository.py
│       ├── service.py
│       └── cli.py
├── tests/
│   ├── test_service.py
│   └── test_cli.py
├── README.md
└── pyproject.toml
```

This matches the recommended layout from Chapter 5 — `src/` for the package, `tests/` alongside it, nothing scattered at the repository root.

`pyproject.toml` describes the project to Python's packaging tools. It names the package, declares `pytest` as a development dependency, and creates a `notes` command that runs the `main` function in `cli.py`:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "notes-manager"
version = "0.1.0"
description = "A simple command-line notes manager with local JSON persistence"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
notes = "notes_manager.cli:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

The `pythonpath` setting lets pytest import the package from `src/`, so the tests run without any extra setup.

Install the project into a *virtual environment*, a private folder of Python packages for this project only, so nothing you install here affects other projects:

```bash
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

The `-e` flag makes the install *editable*: the `notes` command runs your source files directly, so changes take effect without reinstalling. The `notes` command won't work until you write `cli.py` in Step 6.

The install also creates a `src/notes_manager.egg-info/` folder of package metadata, and running Python and pytest creates `__pycache__/` and `.pytest_cache/` folders. All of these are generated, so keep them out of git:

```bash
printf ".venv/\n*.egg-info/\n__pycache__/\n.pytest_cache/\n" > .gitignore
git add pyproject.toml .gitignore src/notes_manager/__init__.py
git commit -m "Add project skeleton and pyproject.toml"
```

---

## 6.2 Step 2 — The Data Model

```python
# src/notes_manager/models.py
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid


@dataclass
class Note:
    title: str
    body: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Note":
        return Note(
            id=data["id"],
            title=data["title"],
            body=data["body"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
```

A UUID for `id` rather than an auto-incrementing integer is a deliberate choice here — it avoids any coordination problem if this ever needs to sync across devices, which is exactly the kind of small design decision worth making explicitly rather than letting an AI assistant default to whatever's most common in its training data.

```bash
git add src/notes_manager/models.py
git commit -m "Add Note data model"
```

---

## 6.3 Step 3 — Storage (Repository Layer)

```python
# src/notes_manager/repository.py
import json
from pathlib import Path
from typing import Optional
from .models import Note


class NoteRepository:
    """Handles persistence of notes to a local JSON file."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        if not self.storage_path.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self._write([])

    def _read(self) -> list[dict]:
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _write(self, notes: list[dict]) -> None:
        with open(self.storage_path, "w") as f:
            json.dump(notes, f, indent=2)

    def add(self, note: Note) -> Note:
        notes = self._read()
        notes.append(note.to_dict())
        self._write(notes)
        return note

    def get(self, note_id: str) -> Optional[Note]:
        notes = self._read()
        for n in notes:
            if n["id"] == note_id:
                return Note.from_dict(n)
        return None

    def list_all(self) -> list[Note]:
        return [Note.from_dict(n) for n in self._read()]

    def update(self, note: Note) -> Optional[Note]:
        notes = self._read()
        for i, n in enumerate(notes):
            if n["id"] == note.id:
                notes[i] = note.to_dict()
                self._write(notes)
                return note
        return None

    def delete(self, note_id: str) -> bool:
        notes = self._read()
        filtered = [n for n in notes if n["id"] != note_id]
        if len(filtered) == len(notes):
            return False
        self._write(filtered)
        return True
```

```bash
git add src/notes_manager/repository.py
git commit -m "Add JSON-backed note repository"
```

Note the read-modify-write pattern here is intentionally simple, not optimized — for a single-user local CLI tool, this is the right level of engineering effort. Reaching for SQLite or a database library here would be over-engineering relative to the actual requirement. That judgment call — matching implementation complexity to actual need — is exactly the kind of thing worth deciding deliberately rather than letting AI default to the most "impressive" solution.

---

## 6.4 Step 4 — Business Logic (Service Layer)

```python
# src/notes_manager/service.py
from datetime import datetime, timezone
from typing import Optional
from .models import Note
from .repository import NoteRepository


class NoteNotFoundError(Exception):
    pass


class AmbiguousNoteIdError(Exception):
    pass


class NoteService:
    """Business logic layer, independent of storage and CLI details."""

    def __init__(self, repository: NoteRepository):
        self.repository = repository

    def create_note(self, title: str, body: str) -> Note:
        if not title.strip():
            raise ValueError("Note title cannot be empty")
        note = Note(title=title.strip(), body=body)
        return self.repository.add(note)

    def get_note(self, note_id: str) -> Note:
        note = self.repository.get(note_id)
        if note is None:
            raise NoteNotFoundError(f"No note found with id {note_id}")
        return note

    def find_by_prefix(self, prefix: str) -> Note:
        """Return the one note whose id starts with prefix."""
        if not prefix:
            raise ValueError("Note id prefix cannot be empty")
        matches = [n for n in self.repository.list_all() if n.id.startswith(prefix)]
        if not matches:
            raise NoteNotFoundError(f"No note found starting with {prefix}")
        if len(matches) > 1:
            raise AmbiguousNoteIdError(
                f"{len(matches)} notes start with {prefix}; type more of the id"
            )
        return matches[0]

    def list_notes(self) -> list[Note]:
        return self.repository.list_all()

    def edit_note(self, note_id: str, title: Optional[str] = None, body: Optional[str] = None) -> Note:
        note = self.get_note(note_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Note title cannot be empty")
            note.title = title.strip()
        if body is not None:
            note.body = body
        note.updated_at = datetime.now(timezone.utc).isoformat()
        updated = self.repository.update(note)
        if updated is None:
            raise NoteNotFoundError(f"No note found with id {note_id}")
        return updated

    def delete_note(self, note_id: str) -> None:
        if not self.repository.delete(note_id):
            raise NoteNotFoundError(f"No note found with id {note_id}")

    def search_notes(self, query: str) -> list[Note]:
        query_lower = query.lower()
        return [
            n for n in self.repository.list_all()
            if query_lower in n.title.lower() or query_lower in n.body.lower()
        ]
```

```bash
git add src/notes_manager/service.py
git commit -m "Add note service with validation and search"
```

The empty-title validation is a good example of a requirement that's easy for AI to skip if you don't ask for it explicitly, and easy to forget to test if you don't notice it's missing — which is exactly why it's called out here and covered directly in the test suite below.

`find_by_prefix` lets users type the first few characters of a note's ID instead of the whole UUID. It refuses a prefix that matches more than one note. The obvious version, "take the first match", would let `notes delete a` silently delete whichever note starting with `a` happened to be stored first.

---

## 6.5 Step 5 — Tests

Business logic isolated from I/O (Section 6.4) means these tests run against a real repository backed by a temporary file, with no mocking required:

```python
# tests/test_service.py
import pytest
from pathlib import Path
from notes_manager.models import Note
from notes_manager.repository import NoteRepository
from notes_manager.service import AmbiguousNoteIdError, NoteNotFoundError, NoteService


@pytest.fixture
def service(tmp_path: Path) -> NoteService:
    repo = NoteRepository(tmp_path / "notes.json")
    return NoteService(repo)


class TestCreateNote:
    def test_creates_note_with_title_and_body(self, service):
        note = service.create_note("Title", "Body")
        assert note.title == "Title"
        assert note.body == "Body"
        assert note.id is not None

    def test_rejects_empty_title(self, service):
        with pytest.raises(ValueError):
            service.create_note("   ", "Body")


class TestGetAndListNotes:
    def test_get_returns_saved_note(self, service):
        note = service.create_note("Title", "Body")
        assert service.get_note(note.id) == note

    def test_get_raises_for_missing_note(self, service):
        with pytest.raises(NoteNotFoundError):
            service.get_note("does-not-exist")

    def test_list_is_empty_at_start(self, service):
        assert service.list_notes() == []

    def test_list_returns_all_notes(self, service):
        service.create_note("First", "a")
        service.create_note("Second", "b")
        assert [n.title for n in service.list_notes()] == ["First", "Second"]


class TestFindByPrefix:
    def test_finds_unique_prefix(self, service):
        note = service.create_note("Title", "Body")
        assert service.find_by_prefix(note.id[:8]).id == note.id

    def test_rejects_ambiguous_prefix(self, service):
        service.repository.add(Note(title="One", body="", id="abc111"))
        service.repository.add(Note(title="Two", body="", id="abc222"))
        with pytest.raises(AmbiguousNoteIdError):
            service.find_by_prefix("abc")

    def test_raises_for_unknown_prefix(self, service):
        with pytest.raises(NoteNotFoundError):
            service.find_by_prefix("zzz")


class TestEditNote:
    def test_edit_updates_title_and_body(self, service):
        note = service.create_note("Original", "old body")
        updated = service.edit_note(note.id, title="Changed", body="new body")
        assert updated.title == "Changed"
        assert updated.body == "new body"

    def test_edit_title_only_keeps_body(self, service):
        note = service.create_note("Original", "body")
        updated = service.edit_note(note.id, title="Changed")
        assert updated.title == "Changed"
        assert updated.body == "body"

    def test_edit_raises_for_missing_note(self, service):
        with pytest.raises(NoteNotFoundError):
            service.edit_note("does-not-exist", title="x")


class TestDeleteNote:
    def test_delete_removes_note(self, service):
        note = service.create_note("Temp", "body")
        service.delete_note(note.id)
        with pytest.raises(NoteNotFoundError):
            service.get_note(note.id)


class TestSearchNotes:
    def test_search_matches_title(self, service):
        service.create_note("Groceries", "milk and eggs")
        service.create_note("Work", "finish the report")
        results = service.search_notes("grocer")
        assert len(results) == 1
        assert results[0].title == "Groceries"

    def test_search_matches_body(self, service):
        service.create_note("Note A", "mentions raspberry pi")
        assert len(service.search_notes("raspberry")) == 1
```

Run the service tests. The output below was pasted from a real run of this code:

```bash
python3 -m pytest tests/test_service.py -v --no-header
```

```text
============================= test session starts ==============================
collecting ... collected 15 items

tests/test_service.py::TestCreateNote::test_creates_note_with_title_and_body PASSED [  6%]
tests/test_service.py::TestCreateNote::test_rejects_empty_title PASSED   [ 13%]
tests/test_service.py::TestGetAndListNotes::test_get_returns_saved_note PASSED [ 20%]
tests/test_service.py::TestGetAndListNotes::test_get_raises_for_missing_note PASSED [ 26%]
tests/test_service.py::TestGetAndListNotes::test_list_is_empty_at_start PASSED [ 33%]
tests/test_service.py::TestGetAndListNotes::test_list_returns_all_notes PASSED [ 40%]
tests/test_service.py::TestFindByPrefix::test_finds_unique_prefix PASSED [ 46%]
tests/test_service.py::TestFindByPrefix::test_rejects_ambiguous_prefix PASSED [ 53%]
tests/test_service.py::TestFindByPrefix::test_raises_for_unknown_prefix PASSED [ 60%]
tests/test_service.py::TestEditNote::test_edit_updates_title_and_body PASSED [ 66%]
tests/test_service.py::TestEditNote::test_edit_title_only_keeps_body PASSED [ 73%]
tests/test_service.py::TestEditNote::test_edit_raises_for_missing_note PASSED [ 80%]
tests/test_service.py::TestDeleteNote::test_delete_removes_note PASSED   [ 86%]
tests/test_service.py::TestSearchNotes::test_search_matches_title PASSED [ 93%]
tests/test_service.py::TestSearchNotes::test_search_matches_body PASSED  [100%]

============================== 15 passed in 0.05s ==============================
```

`--no-header` hides the lines that show your Python version and file paths, so your output should match this apart from the timing.

```bash
git add tests/test_service.py
git commit -m "Add service layer test suite"
```

---

## 6.6 Step 6 — The CLI Layer

```python
# src/notes_manager/cli.py
import argparse
import sys
from pathlib import Path
from .repository import NoteRepository
from .service import AmbiguousNoteIdError, NoteNotFoundError, NoteService

DEFAULT_STORAGE = Path.home() / ".notes-manager" / "notes.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notes", description="A simple CLI notes manager")
    parser.add_argument("--storage", type=Path, default=DEFAULT_STORAGE)
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new note")
    add_p.add_argument("title")
    add_p.add_argument("body")

    sub.add_parser("list", help="List all notes")

    edit_p = sub.add_parser("edit", help="Edit an existing note")
    edit_p.add_argument("id")
    edit_p.add_argument("--title")
    edit_p.add_argument("--body")

    delete_p = sub.add_parser("delete", help="Delete a note")
    delete_p.add_argument("id")

    search_p = sub.add_parser("search", help="Search notes by title or body")
    search_p.add_argument("query")

    return parser


def format_note(note) -> str:
    return f"[{note.id[:8]}] {note.title}\n    {note.body}\n    updated: {note.updated_at}"


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = NoteRepository(args.storage)
    service = NoteService(repo)

    try:
        if args.command == "add":
            note = service.create_note(args.title, args.body)
            print(f"Created note {note.id[:8]}")
        elif args.command == "list":
            notes = service.list_notes()
            print("No notes yet." if not notes else "\n".join(format_note(n) for n in notes))
        elif args.command == "edit":
            match = service.find_by_prefix(args.id)
            note = service.edit_note(match.id, title=args.title, body=args.body)
            print(f"Updated note {note.id[:8]}")
        elif args.command == "delete":
            match = service.find_by_prefix(args.id)
            service.delete_note(match.id)
            print(f"Deleted note {match.id[:8]}")
        elif args.command == "search":
            results = service.search_notes(args.query)
            print("No matches." if not results else "\n".join(format_note(n) for n in results))
    except (NoteNotFoundError, AmbiguousNoteIdError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

```bash
git add src/notes_manager/cli.py
git commit -m "Add CLI layer for notes manager"
```

`main` returns `0` on success and `1` on an error. The `notes` command that `pyproject.toml` creates passes that number back to your shell as the exit code, which is how scripts and CI tell success from failure.

The CLI needs tests too. Calling `main([...])` with a list of arguments runs the CLI inside the test process. pytest's `capsys` fixture captures what it prints, and `tmp_path` gives each test its own storage file:

```python
# tests/test_cli.py
import pytest
from pathlib import Path
from notes_manager.cli import main
from notes_manager.models import Note
from notes_manager.repository import NoteRepository


@pytest.fixture
def storage(tmp_path: Path) -> Path:
    return tmp_path / "notes.json"


def run(storage: Path, *args: str) -> int:
    return main(["--storage", str(storage), *args])


def test_add_then_list(storage, capsys):
    assert run(storage, "add", "Groceries", "milk") == 0
    assert run(storage, "list") == 0
    out = capsys.readouterr().out
    assert "Created note" in out
    assert "Groceries" in out


def test_list_when_empty(storage, capsys):
    assert run(storage, "list") == 0
    assert capsys.readouterr().out == "No notes yet.\n"


def test_edit_by_prefix(storage, capsys):
    run(storage, "add", "Old", "body")
    note_id = NoteRepository(storage).list_all()[0].id
    assert run(storage, "edit", note_id[:8], "--title", "New") == 0
    assert NoteRepository(storage).get(note_id).title == "New"


def test_delete_unknown_id_fails(storage, capsys):
    assert run(storage, "delete", "zzz") == 1
    assert "Error: No note found" in capsys.readouterr().err


def test_delete_ambiguous_prefix_deletes_nothing(storage, capsys):
    repo = NoteRepository(storage)
    repo.add(Note(title="One", body="", id="abc111"))
    repo.add(Note(title="Two", body="", id="abc222"))
    assert run(storage, "delete", "abc") == 1
    assert "2 notes start with abc" in capsys.readouterr().err
    assert len(repo.list_all()) == 2


def test_search_reports_no_matches(storage, capsys):
    run(storage, "add", "Groceries", "milk")
    capsys.readouterr()
    assert run(storage, "search", "report") == 0
    assert capsys.readouterr().out == "No matches.\n"
```

The last two tests in the file check error handling: an unknown ID and an ambiguous prefix must both fail with exit code `1`, and the ambiguous one must not delete anything. Run the whole suite:

```bash
python3 -m pytest --no-header
```

```text
============================= test session starts ==============================
collected 21 items

tests/test_cli.py ......                                                 [ 28%]
tests/test_service.py ...............                                    [100%]

============================== 21 passed in 0.07s ==============================
```

```bash
git add tests/test_cli.py
git commit -m "Add CLI tests"
```

### Trying it out

With the project installed (Step 1), the `notes` command is on your path. These examples use `--storage demo.json` so they don't touch your real notes in `~/.notes-manager/`. This is real output from the finished CLI. Your IDs and timestamps will be different:

```bash
notes --storage demo.json add "Groceries" "Milk, eggs, bread"
notes --storage demo.json add "Book club" "Read chapter 6 by Friday"
notes --storage demo.json list
```

```text
Created note adacf9c0
Created note 2b224d33
[adacf9c0] Groceries
    Milk, eggs, bread
    updated: 2026-10-02T18:02:39.893221+00:00
[2b224d33] Book club
    Read chapter 6 by Friday
    updated: 2026-10-02T18:02:39.963146+00:00
```

```bash
notes --storage demo.json search "milk"
```

```text
[adacf9c0] Groceries
    Milk, eggs, bread
    updated: 2026-10-02T18:02:39.893221+00:00
```

`edit` and `delete` accept any unique start of an ID:

```bash
notes --storage demo.json edit adac --body "Milk, eggs, bread, coffee"
notes --storage demo.json delete 2b22
notes --storage demo.json list
```

```text
Updated note adacf9c0
Deleted note 2b224d33
[adacf9c0] Groceries
    Milk, eggs, bread, coffee
    updated: 2026-10-02T18:02:43.897872+00:00
```

Deleting the same note again fails, with exit code `1`:

```bash
notes --storage demo.json delete 2b22
```

```text
Error: No note found starting with 2b22
```

> **Screenshot placeholder:** Capture your own terminal running these same commands, plus `edit` and `delete`, and insert it here in the published version alongside this verified transcript.

---

## 6.7 Step 7 — Documentation

A minimal but complete `README.md`:

```markdown
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
```

```bash
git add README.md
git commit -m "Add project README"
```

---

## Engineering Insight

> Small iterations combined with continuous testing produce more reliable AI-assisted software than one-shot generation — the eight commits in this chapter could have been one AI-generated dump, and the difference in review quality between those two approaches is the entire argument of this book.

---

## Common Mistakes

- Large, single commits that bundle model, storage, service, and CLI together, making review meaningless.
- Missing tests for validation logic (the empty-title check) because it's easy to overlook when the happy path works.
- No documentation, leaving the next person — including future you — to reverse-engineer usage from the code.
- Blind acceptance of AI output without running it, as demonstrated by actually executing every command in this chapter before publishing it.

---

## Hands-On Lab: Extend the Notes Manager

Using the same workflow — one small piece at a time, tested and committed individually — extend the application with:

1. **Tags**: add a `tags: list[str]` field to `Note`, and a `notes tag <id> <tag>` command.
2. **Categories**: a single `category: str` field with a `notes list --category <name>` filter.
3. **Import/export**: `notes export backup.json` and `notes import backup.json`, handling ID collisions explicitly.
4. **Sorting**: `notes list --sort-by updated_at|title`.

For each feature, follow the same cycle used throughout this chapter: clarify the requirement, implement it in the appropriate layer (model, repository, service, or CLI), write tests before considering it done, and commit independently. Run the full test suite after each addition to confirm nothing earlier broke:

```bash
python3 -m pytest tests/ -v
```

---

## Chapter Summary

This project demonstrated the complete AI-assisted workflow from requirements through tested, documented, deployment-ready code — layered architecture, incremental commits, a real passing test suite, and documentation that matches what the code actually does. Every command and test result shown in this chapter was verified by actually running it, which is the standard every AI-assisted change in your own projects should be held to as well.

---

## Review Questions

1. Why build incrementally rather than generating the whole application in one AI request?
2. Why validate AI-generated output with automated tests rather than a visual read-through?
3. Why document continuously instead of writing the README after the code is "done"?
4. What belongs in a project README, and what's the cost of a README that overstates what the code does?
5. Why does separating the service layer from the repository and CLI make testing — and AI-assisted development generally — easier?

---

## End of Part 1

Part 2 (Volume 2) begins with [prompt](../glossary.md#prompt) engineering and effective communication with AI systems — building directly on the context and workflow habits established across these first six chapters.

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

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

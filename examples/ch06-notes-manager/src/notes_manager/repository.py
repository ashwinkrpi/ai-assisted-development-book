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
        with open(self.storage_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, notes: list[dict]) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
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

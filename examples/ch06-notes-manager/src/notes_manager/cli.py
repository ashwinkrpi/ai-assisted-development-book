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
    body = note.body.replace("\n", "\n    ")
    return f"[{note.id[:8]}] {note.title}\n    {body}\n    updated: {note.updated_at}"


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = NoteRepository(args.storage.expanduser())
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

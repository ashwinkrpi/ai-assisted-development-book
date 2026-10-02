"""Check that code blocks in the chapters match the files in examples/.

A fenced block is checked when its first line is a comment naming a file,
such as "# tests/test_cli.py". The file is looked up in the example folder
for that chapter (examples/chNN-*/). Exits with status 1 on any mismatch.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.S | re.M)
PATH_COMMENT = re.compile(r"# ([\w./-]+\.(?:py|toml))\n")

# Blocks that can't carry a path comment: (chapter number, block's first line) -> file
EXTRA = {(6, "# Notes Manager"): "README.md"}


def main() -> int:
    errors = []
    checked = 0
    for chapter in sorted((ROOT / "chapters").glob("*/[0-9][0-9]-*.md")):
        number = int(chapter.name[:2])
        folders = list((ROOT / "examples").glob(f"ch{number:02d}-*"))
        if not folders:
            continue
        example = folders[0]
        for match in FENCE.finditer(chapter.read_text()):
            block = match.group(2)
            first_line = block.split("\n", 1)[0]
            name = EXTRA.get((number, first_line))
            if name is None:
                path_match = PATH_COMMENT.match(block)
                if not path_match:
                    continue
                name = path_match.group(1)
            target = example / name
            checked += 1
            if not target.exists():
                errors.append(f"{chapter.name}: {name} not found in {example.name}/")
            elif target.read_text() != block:
                errors.append(f"{chapter.name}: block for {name} differs from {example.name}/{name}")
    for error in errors:
        print(error)
    print(f"Checked {checked} code blocks, {len(errors)} mismatches.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

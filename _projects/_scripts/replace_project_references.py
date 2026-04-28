#!/usr/bin/env python3
"""
Replace project path references when a project is moved to _projects/.completed/.

Performs a global literal find-and-replace of:
    _projects/{folder}  -->  _projects/.completed/{folder}

across every text file in the _projects/ tree (including .completed/, .on-hold/,
.shelved/, _rules/, and _scripts/). Handles self-references, parent-child
cross-references, sibling sub-project references, and unrelated project
references in a single pass.

Double-replacement is impossible: the replacement text
"_projects/.completed/{folder}" does not contain the search text
"_projects/{folder}" as a substring because the ".completed/" segment
breaks the match.

Usage:
    # Dry run (preview changes without writing)
    python3 _projects/_scripts/replace_project_references.py \
        --folder "20260225.01.deployment-component-catalog-redesign" --dry-run

    # Apply changes
    python3 _projects/_scripts/replace_project_references.py \
        --folder "20260225.01.deployment-component-catalog-redesign"

    # Retroactive fix for all completed projects
    for dir in _projects/.completed/*/; do
        folder=$(basename "$dir")
        python3 _projects/_scripts/replace_project_references.py \
            --folder "$folder"
    done
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".pdf", ".zip", ".gz", ".tar", ".bz2", ".7z",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe",
    ".lock",
})


def resolve_repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("Error: could not determine repo root. Pass --repo-root explicitly.")


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return False
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
        return b"\x00" not in chunk
    except OSError:
        return False


def replace_in_file(path: Path, search: str, replacement: str, dry_run: bool) -> int:
    """Replace all occurrences of search with replacement in a single file.

    Returns the number of replacements made (0 if the file was unchanged).
    """
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0

    count = content.count(search)
    if count == 0:
        return 0

    if not dry_run:
        new_content = content.replace(search, replacement)
        path.write_text(new_content, encoding="utf-8")

    return count


def run(folder: str, repo_root: Path, dry_run: bool) -> None:
    projects_dir = repo_root / "_projects"
    if not projects_dir.is_dir():
        sys.exit(f"Error: {projects_dir} is not a directory.")

    search = f"_projects/{folder}"
    replacement = f"_projects/.completed/{folder}"

    files_scanned = 0
    files_changed = 0
    total_replacements = 0
    changed_files: list[tuple[Path, int]] = []

    for root, _dirs, filenames in os.walk(projects_dir):
        for filename in filenames:
            filepath = Path(root) / filename
            if not is_text_file(filepath):
                continue

            files_scanned += 1
            count = replace_in_file(filepath, search, replacement, dry_run)
            if count > 0:
                files_changed += 1
                total_replacements += count
                rel = filepath.relative_to(repo_root)
                changed_files.append((rel, count))

    mode = "DRY RUN" if dry_run else "APPLIED"
    print(f"\n--- {mode}: replace_project_references ---")
    print(f"  Folder:       {folder}")
    print(f"  Search:       {search}")
    print(f"  Replacement:  {replacement}")
    print(f"  Files scanned:      {files_scanned}")
    print(f"  Files changed:      {files_changed}")
    print(f"  Total replacements: {total_replacements}")

    if changed_files:
        print(f"\n  Changed files:")
        for rel, count in sorted(changed_files):
            print(f"    {rel}  ({count} replacement{'s' if count != 1 else ''})")

    if files_changed == 0:
        print(f"\n  No references to '{search}' found. Nothing to do.")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replace _projects/{folder} with _projects/.completed/{folder} "
                    "across the entire _projects/ tree.",
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Project folder name (e.g. '20260225.01.deployment-component-catalog-redesign'). "
             "Do NOT include '_projects/' prefix.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repo root directory. Defaults to git rev-parse --show-toplevel.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to disk.",
    )
    args = parser.parse_args()

    if "/" in args.folder or args.folder.startswith("."):
        sys.exit(
            f"Error: --folder should be the bare folder name "
            f"(e.g. '20260225.01.my-project'), not a path. Got: '{args.folder}'"
        )

    repo_root = resolve_repo_root(args.repo_root)
    run(args.folder, repo_root, args.dry_run)


if __name__ == "__main__":
    main()

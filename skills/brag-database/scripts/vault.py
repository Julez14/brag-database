#!/usr/bin/env python3
"""Local destination management only; historical evidence comes from cloud MCP."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


def config_path():
    return Path(os.environ.get("BRAG_DATABASE_CONFIG", "~/.config/brag-database/config.json")).expanduser()


def load_config():
    config = json.loads(config_path().read_text())
    vault = Path(config["vault_path"]).expanduser().resolve(strict=True)
    if not (vault / ".obsidian").is_dir():
        raise ValueError("Configured destination is not an Obsidian vault")
    return config, vault


def note_path(vault, relative):
    path = Path(relative)
    if path.is_absolute() or not path.parts or any(p.startswith(".") for p in path.parts):
        raise ValueError("Use a relative note path without hidden folders or traversal")
    if path.suffix.lower() != ".md":
        raise ValueError("Only Markdown notes can be saved")
    resolved = (vault / path).resolve()
    if not resolved.is_relative_to(vault):
        raise ValueError("Destination escapes the vault")
    return resolved


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_note(vault, payload):
    target = note_path(vault, payload["path"])
    content = payload["content"]
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Note content must be nonempty text")
    expected = payload.get("expected_sha256")
    if target.exists():
        if expected is None or digest(target.read_bytes()) != expected:
            raise ValueError("Note exists or changed; read it and supply its current expected_sha256")
    elif expected is not None:
        raise ValueError("The note to revise no longer exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    # Non-Markdown temporary file in the same directory: templates never see an empty note.
    fd, temporary = tempfile.mkstemp(prefix=".brag-", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content.encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        if expected is None:
            os.link(temporary, target)  # Exclusive, complete creation; no clobber.
        else:
            if not target.exists() or digest(target.read_bytes()) != expected:
                raise ValueError("Note changed during save; reread before retrying")
            os.chmod(temporary, target.stat().st_mode & 0o777)
            os.replace(temporary, target)
        return {"path": str(target), "sha256": digest(content.encode("utf-8")), "cloud_sync": "not verified"}
    finally:
        Path(temporary).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("describe")
    read = commands.add_parser("read", help="Read a destination note before revising it")
    read.add_argument("--path", required=True)
    commands.add_parser("save", help="Read {path, content, expected_sha256?} JSON from stdin")
    args = parser.parse_args()
    config, vault = load_config()
    if args.command == "describe":
        result = {"vault_path": str(vault), "cloud": config.get("cloud", {}),
                  "folders": config.get("folders", {}),
                  "notes": sorted(str(p.relative_to(vault)) for p in vault.rglob("*.md")
                                  if not any(x.startswith(".") for x in p.relative_to(vault).parts))}
    elif args.command == "read":
        path = note_path(vault, args.path)
        data = path.read_bytes()
        result = {"path": str(path), "sha256": digest(data), "content": data.decode("utf-8")}
    else:
        result = save_note(vault, json.load(sys.stdin))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"brag-database: {exc}", file=sys.stderr)
        sys.exit(1)

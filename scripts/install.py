#!/usr/bin/env python3
"""Install the drafting skill and remember this machine's vault destination."""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = {"career": "Career", "clubs": "Clubs", "scholarships": "Scholarships and Grants",
           "hackathons": "Hackathons", "school": "School", "interview": "Interview Prep"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--account-id")
    parser.add_argument("--instance")
    parser.add_argument("--namespace")
    parser.add_argument("--bucket")
    parser.add_argument("--prefix")
    args = parser.parse_args()
    vault = args.vault.expanduser().resolve(strict=True)
    if not (vault / ".obsidian").is_dir():
        parser.error("Open this folder as an Obsidian vault first")
    if vault == ROOT or ROOT in vault.parents or vault in ROOT.parents:
        parser.error("The personal vault and public repository must be separate")
    config_path = Path(os.environ.get("BRAG_DATABASE_CONFIG", "~/.config/brag-database/config.json")).expanduser()
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    config["vault_path"] = str(vault)
    config.setdefault("folders", FOLDERS.copy())
    cloud = config.setdefault("cloud", {"account_id": "", "namespace": "default",
                                       "instance_id": "brag-database", "bucket": "brag-database",
                                       "prefix": "vault/"})
    for arg, key in [("account_id", "account_id"), ("instance", "instance_id"),
                     ("namespace", "namespace"), ("bucket", "bucket"), ("prefix", "prefix")]:
        value = getattr(args, arg)
        if value is not None:
            cloud[key] = value
    source = ROOT / "skills/brag-database"
    destination = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills/brag-database"
    if destination.exists() or destination.is_symlink():
        if not destination.is_symlink() or destination.resolve() != source:
            parser.error(f"Existing skill at {destination}; move it aside before installing")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source, target_is_directory=True)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".config-", dir=config_path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(config, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, config_path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print(f"Skill: {destination}\nSettings: {config_path}\nVault: {vault}")
    print("Cloud account: " + (cloud.get("account_id") or "not configured"))
    print("Open a new Codex conversation to discover the skill. Cloud setup is separate; see docs/setup.md.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        sys.exit(1)

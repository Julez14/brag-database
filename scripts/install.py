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
           "hackathons": "Hackathons", "school": "School", "interview": "Interview Prep",
           "resumes": "Resumes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--account-id")
    parser.add_argument("--instance")
    parser.add_argument("--namespace")
    parser.add_argument("--bucket")
    parser.add_argument("--prefix")
    parser.add_argument("--with-resume-builder", action="store_true",
                        help="Also install the optional resume-builder skill")
    args = parser.parse_args()
    vault = args.vault.expanduser().resolve(strict=True)
    if not (vault / ".obsidian").is_dir():
        parser.error("Open this folder as an Obsidian vault first")
    if vault == ROOT or ROOT in vault.parents or vault in ROOT.parents:
        parser.error("The personal vault and public repository must be separate")
    config_path = Path(os.environ.get("BRAG_DATABASE_CONFIG", "~/.config/brag-database/config.json")).expanduser()
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    config["vault_path"] = str(vault)
    folders = config.setdefault("folders", FOLDERS.copy())
    folders.setdefault("resumes", "Resumes")
    cloud = config.setdefault("cloud", {"account_id": "", "namespace": "default",
                                       "instance_id": "brag-database", "bucket": "brag-database",
                                       "prefix": "vault/"})
    for arg, key in [("account_id", "account_id"), ("instance", "instance_id"),
                     ("namespace", "namespace"), ("bucket", "bucket"), ("prefix", "prefix")]:
        value = getattr(args, arg)
        if value is not None:
            cloud[key] = value
    skills = ["brag-database"]
    if args.with_resume_builder:
        skills.append("resume-builder")
    skill_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    for skill in skills:
        source = ROOT / "skills" / skill
        destination = skill_home / skill
        if destination.exists() or destination.is_symlink():
            if not destination.is_symlink() or destination.resolve() != source:
                parser.error(f"Existing skill at {destination}; move it aside before installing")
    skill_home.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        destination = skill_home / skill
        if not destination.is_symlink():
            destination.symlink_to(ROOT / "skills" / skill, target_is_directory=True)
    if args.with_resume_builder:
        resume_folder = (vault / folders["resumes"]).resolve()
        if not resume_folder.is_relative_to(vault):
            parser.error("Resume folder must be inside the vault")
        resume_folder.mkdir(parents=True, exist_ok=True)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".config-", dir=config_path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(config, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, config_path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print("Skills: " + ", ".join(str(skill_home / skill) for skill in skills))
    print(f"Settings: {config_path}\nVault: {vault}")
    print("Cloud account: " + (cloud.get("account_id") or "not configured"))
    print("Open a new Codex conversation to discover the skill. Cloud setup is separate; see docs/setup.md.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        sys.exit(1)

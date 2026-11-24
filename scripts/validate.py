"""Check marketplace.json against the format VTCode reads (stdlib only).

Usage: python scripts/validate.py [marketplace.json]
"""
import json
import re
import sys

REPO = re.compile(r"^https://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
ID = re.compile(r"^[a-z0-9][a-z0-9-]*\.[a-z0-9][a-z0-9.-]*$")
ENTRY_KEYS = {"id", "repository", "name", "description"}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    for key in ("name", "description"):
        if key in data and not isinstance(data[key], str):
            errors.append(f"{key} must be a string")
    entries = data.get("extensions")
    if not isinstance(entries, list):
        return errors + ["extensions must be a list"]
    ids, repos = set(), set()
    for index, entry in enumerate(entries):
        where = f"extensions[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{where} must be an object")
            continue
        unknown = set(entry) - ENTRY_KEYS
        if unknown:
            errors.append(f"{where} has unknown keys: {sorted(unknown)}")
        ext_id, repo = entry.get("id"), entry.get("repository")
        if not isinstance(ext_id, str) or not ID.match(ext_id):
            errors.append(f"{where}.id must look like publisher.name")
        elif ext_id in ids:
            errors.append(f"{where}.id {ext_id} is listed twice")
        else:
            ids.add(ext_id)
        if not isinstance(repo, str) or not REPO.match(repo):
            errors.append(f"{where}.repository must be https://github.com/owner/repo")
        elif repo.lower() in repos:
            errors.append(f"{where}.repository {repo} is listed twice")
        else:
            repos.add(repo.lower())
        for key in ("name", "description"):
            if key in entry and not isinstance(entry[key], str):
                errors.append(f"{where}.{key} must be a string")
    listed = [e.get("id", "") for e in entries if isinstance(e, dict)]
    if listed != sorted(listed):
        errors.append("extensions must be sorted by id")
    return errors


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "marketplace.json"
    with open(path, encoding="utf-8") as handle:
        errors = validate(json.load(handle))
    for error in errors:
        print(f"{path}: {error}")
    if errors:
        sys.exit(1)
    print(f"{path}: OK")


if __name__ == "__main__":
    main()

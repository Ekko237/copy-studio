#!/usr/bin/env python3
"""Check SKILL.md frontmatter against the Agent Skills spec.

Fails when name is missing or description is empty or longer than 1024 characters.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "copy-studio" / "SKILL.md"
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500


def fail(errors):
    for error in errors:
        print("✗", error)
    print(f"{len(errors)} problem(s)")
    sys.exit(1)


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        body = value[1:-1]
        if value[0] == "'":
            return body.replace("''", "'")
        return body.replace('\\"', '"').replace("\\n", "\n")
    return value


def main():
    errors = []
    skill_files = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.glob("**/SKILL.md"))
    if skill_files != ["skills/copy-studio/SKILL.md"]:
        errors.append(
            "expected exactly skills/copy-studio/SKILL.md, found "
            + (", ".join(skill_files) if skill_files else "none")
        )

    claude_plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if "skills" in claude_plugin:
        errors.append("Claude plugin.json must not set skills; skills/copy-studio is the default scan")
    if claude_plugin.get("commands") != []:
        errors.append("Claude plugin.json must set commands to [] so commands/copy-studio.md is not a second skill")

    codex_plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if codex_plugin.get("skills") != "./skills/":
        errors.append('Codex plugin.json skills must be "./skills/"')

    if errors:
        fail(errors)

    text = SKILL.read_text(encoding="utf-8")
    errors = []
    if not text.startswith("---\n"):
        fail(["SKILL.md is missing frontmatter"])
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(["SKILL.md frontmatter is not closed"])
    raw = text[4:end]

    name_match = re.search(r"^name:\s*(\S+)\s*$", raw, re.M)
    if not name_match:
        errors.append("frontmatter name is missing")
        name = ""
    else:
        name = unquote(name_match.group(1))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"name {name!r} is not lowercase words separated by single hyphens")
        if name != SKILL.parent.name:
            errors.append(
                f"name {name!r} does not match the parent directory {SKILL.parent.name!r}"
            )

    desc_match = re.search(r"^description:\s*(\S.*)$", raw, re.M)
    if not desc_match:
        errors.append("frontmatter description is missing")
    else:
        description = unquote(desc_match.group(1))
        length = len(description)
        print(f"description: {length} characters")
        if length == 0:
            errors.append("description is empty")
        elif length > MAX_DESCRIPTION:
            errors.append(f"description is {length} characters; the limit is {MAX_DESCRIPTION}")
        if not description.startswith("Use when"):
            errors.append('description must lead with "Use when"')

    if re.search(r"^version\s*:", raw, re.M):
        errors.append("top-level version is not a spec field; put version under metadata")
    if not re.search(r'^metadata:\s*$', raw, re.M):
        errors.append("metadata block is missing")
    if not re.search(r'^  version:\s*(["\'][^"\']+["\'])\s*$', raw, re.M):
        errors.append("metadata.version must be a quoted string")

    compat_match = re.search(r"^compatibility:\s*(\S.*)$", raw, re.M)
    if compat_match:
        compatibility = unquote(compat_match.group(1))
        if len(compatibility) > MAX_COMPATIBILITY:
            errors.append(
                f"compatibility is {len(compatibility)} characters; the limit is {MAX_COMPATIBILITY}"
            )

    if errors:
        fail(errors)
    print("OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the Yunsheng PM skill pack without third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


PACK_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PACK_ROOT / "skills"
MAX_IMPORT_BYTES = 64 * 1024


def frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    match = re.search(
        rf"^{re.escape(key)}:\s*[\"']?([^\n\"']+)[\"']?\s*$",
        text[4:end],
        re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def quoted_yaml_value(text: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*([\"'])(.*?)\1\s*$",
        text,
        re.MULTILINE,
    )
    return match.group(2) if match else None


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((PACK_ROOT / "manifest.json").read_text(encoding="utf-8"))
    expected = manifest["skills"]
    actual = sorted(path.name for path in SKILLS_ROOT.iterdir() if path.is_dir())

    if len(expected) != len(set(expected)):
        errors.append("manifest contains duplicate skill names")
    if sorted(expected) != actual:
        errors.append("manifest skill list does not match skills directory")

    for name in expected:
        skill_dir = SKILLS_ROOT / name
        skill_file = skill_dir / "SKILL.md"
        ui_file = skill_dir / "agents" / "openai.yaml"

        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        if not ui_file.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
            continue

        text = skill_file.read_text(encoding="utf-8")
        ui_text = ui_file.read_text(encoding="utf-8")
        if skill_file.stat().st_size > MAX_IMPORT_BYTES:
            errors.append(f"{name}: SKILL.md exceeds 64 KB")
        if frontmatter_value(text, "name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not frontmatter_value(text, "description"):
            errors.append(f"{name}: missing description")
        if "TODO" in text or "Help with" in ui_text:
            errors.append(f"{name}: unfinished scaffold text")

        short_description = quoted_yaml_value(ui_text, "short_description")
        default_prompt = quoted_yaml_value(ui_text, "default_prompt")
        if short_description is None or not 25 <= len(short_description) <= 64:
            errors.append(f"{name}: short_description must be 25-64 characters")
        if default_prompt is None or f"${name}" not in default_prompt:
            errors.append(f"{name}: default_prompt must mention ${name}")

    case_ids: list[str] = []
    for line_number, line in enumerate(
        (PACK_ROOT / "evals" / "cases.jsonl").read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"eval case line {line_number}: {exc}")
            continue
        case_ids.append(case.get("id", ""))
        if case.get("skill") not in expected:
            errors.append(f"eval case line {line_number}: unknown skill")
    if len(case_ids) != len(set(case_ids)):
        errors.append("eval cases contain duplicate ids")

    report = {
        "pack": manifest["name"],
        "version": manifest["version"],
        "skill_count": len(actual),
        "eval_case_count": len(case_ids),
        "max_import_bytes": MAX_IMPORT_BYTES,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

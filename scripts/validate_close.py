#!/usr/bin/env python3
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "status", "owner", "delegate", "due", "project", "parent", "flow", "next_action", "evidence"}


def validate() -> list[str]:
    errors = []
    snapshot = json.loads((ROOT / "data/live_snapshot.json").read_text())
    manifest = json.loads((ROOT / "manifest.json").read_text())
    stamp = dt.datetime.fromisoformat(snapshot["snapshot_at"].replace("Z", "+00:00"))
    source = dt.datetime.fromisoformat(snapshot["source_updated_at"].replace("Z", "+00:00"))
    if stamp - source > dt.timedelta(hours=1) or stamp < source:
        errors.append("snapshot timestamp is not within one hour of its source")
    ids = [task["id"] for task in snapshot["tasks"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate task IDs")
    for index, task in enumerate(snapshot["tasks"], 1):
        missing = REQUIRED - task.keys()
        if missing:
            errors.append(f"task {index} missing fields: {sorted(missing)}")
        if any(value in (None, "") for value in task.values()):
            errors.append(f"task {index} has implicit unknown value")
    if not snapshot["coverage"]["complete"] and not snapshot["coverage"]["reason"]:
        errors.append("incomplete coverage requires an explicit exception")
    prohibited = ["operating_acceptance", "telegram_delivery", "d1_started", "financial_effect_verified"]
    if any(manifest[key] for key in prohibited):
        errors.append("prohibited operational claim is true before complete acceptance")
    for rel in (manifest["snapshot"], manifest["daily_close"], manifest["weekly_close"]):
        if not (ROOT / rel).is_file():
            errors.append(f"missing manifest artifact: {rel}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        raise SystemExit(1)
    print("PASS: close package is internally consistent and fail-closed")

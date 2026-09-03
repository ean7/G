#!/usr/bin/env python3
"""Independently verify the immutable Unified LMS v1.2 release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

EXPECTED_NAME = "MetaTeam_Learning_System_Unified_v1_2_PREVIEW_RC1.zip"
EXPECTED_SIZE = 33_123_984
EXPECTED_SHA256 = "d1a428622392a2a0f24e1f21f783484a413a6d767d843985214d1376ffa3baae"
EXPECTED_MANIFEST_FILES = 453


def fail(check: str, detail: str) -> None:
    print(json.dumps({"verdict": "HOLD", "check": check, "detail": detail}, ensure_ascii=False))
    raise SystemExit(1)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            fail("manifest-format", f"invalid MANIFEST.sha256 line {number}")
        records.append((parts[0].lower(), parts[1].lstrip("*")))
    return records


def verify(candidate: Path) -> None:
    if candidate.name != EXPECTED_NAME:
        fail("filename", f"expected {EXPECTED_NAME}; got {candidate.name}")
    if not candidate.is_file():
        fail("artifact-access", f"candidate is not readable at {candidate}")
    size = candidate.stat().st_size
    if size != EXPECTED_SIZE:
        fail("size", f"expected {EXPECTED_SIZE}; got {size}")
    actual_hash = digest(candidate)
    if actual_hash != EXPECTED_SHA256:
        fail("sha256", f"expected {EXPECTED_SHA256}; got {actual_hash}")

    with zipfile.ZipFile(candidate) as archive:
        corrupt = archive.testzip()
        if corrupt:
            fail("zip-integrity", f"CRC failure in {corrupt}")
        unsafe = [item.filename for item in archive.infolist() if not safe_member(item.filename)]
        if unsafe:
            fail("safe-extraction", f"unsafe archive member: {unsafe[0]}")
        with tempfile.TemporaryDirectory(prefix="unified-lms-v1.2-") as directory:
            root = Path(directory)
            archive.extractall(root)
            manifests = list(root.rglob("MANIFEST.sha256"))
            if len(manifests) != 1:
                fail("manifest-presence", f"expected one MANIFEST.sha256; got {len(manifests)}")
            records = parse_manifest(manifests[0])
            if len(records) != EXPECTED_MANIFEST_FILES:
                fail("manifest-count", f"expected {EXPECTED_MANIFEST_FILES}; got {len(records)}")
            base = manifests[0].parent
            for expected, relative in records:
                target = base / relative
                if not target.is_file() or digest(target) != expected:
                    fail("manifest-verification", f"missing or mismatched: {relative}")

    print(json.dumps({
        "verdict": "EXACT_BYTES_AND_MANIFEST_PASS",
        "filename": candidate.name,
        "bytes": size,
        "sha256": actual_hash,
        "manifest_files": len(records),
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    verify(args.candidate)


if __name__ == "__main__":
    main()

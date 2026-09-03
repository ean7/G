# NOZ-322 — independent Unified LMS v1.2 gate

## Verdict: HOLD

The exact candidate is not present in this repository or elsewhere in the accessible local workspace. The issue provides a filename, byte count, SHA-256 digest, and claimed manifest count, but no persistent URL/object ID or candidate bytes. Those claims cannot substitute for independent read-back.

This review did not obtain or modify candidate bytes. Remediation belongs to the artifact owner, **Eugenyi Nozhenko**: publish the immutable ZIP at a persistent, reviewer-readable location (or commit it through the approved artifact route), then provide that location to the independent reviewer.

## Expected identity

| Property | Required value |
|---|---|
| Filename | `MetaTeam_Learning_System_Unified_v1_2_PREVIEW_RC1.zip` |
| Bytes | `33,123,984` |
| SHA-256 | `d1a428622392a2a0f24e1f21f783484a413a6d767d843985214d1376ffa3baae` |
| Internal manifest | `453` files |

## Gate status

| Gate | Status | Reason |
|---|---|---|
| Download/read-back exact bytes | BLOCKED | No artifact URL, object ID, or local bytes |
| Size and full SHA-256 | NOT RUN | Requires exact bytes |
| ZIP integrity and clean extraction | NOT RUN | Requires exact bytes |
| Internal manifest 453/453 | NOT RUN | Requires extraction |
| Full test replay | NOT RUN | Requires extracted candidate |
| AI→Trainer 17/17 | NOT RUN | Requires extracted candidate |
| AI recommendations 37/37 | NOT RUN | Requires extracted candidate |
| Measurement regressions | NOT RUN | Requires extracted candidate |
| P0=0 / P1=0 | NOT ESTABLISHED | Required evidence is unavailable |

## Reproduction

The repository includes a standard-library-only verifier. It performs identity checks before extraction, rejects traversal members, extracts to a new temporary directory, verifies ZIP CRC, locates exactly one `MANIFEST.sha256`, requires exactly 453 records, and hashes each manifested file.

```sh
python3 tools/verify_unified_lms_candidate.py /persistent/path/MetaTeam_Learning_System_Unified_v1_2_PREVIEW_RC1.zip
```

Only an `EXACT_BYTES_AND_MANIFEST_PASS` result permits continuing to the candidate's own full QA commands. It is not by itself a claim that the full behavioral suite passed.

"""Pinned reference identities and fail-closed compatibility report gates."""

import hashlib
from pathlib import Path

MODEL_SOURCE_FILES = (
    "lib/model/PoseMamba.py",
    "lib/model/mambablocks.py",
    "lib/model/graph_mixer.py",
    "lib/model/conditioning_routes.py",
    "lib/utils/learning.py",
)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_reference(root, expected, name):
    if set(expected) != set(MODEL_SOURCE_FILES):
        raise RuntimeError(f"{name}: incomplete pinned reference identity")
    actual = {filename: sha256_file(Path(root) / filename) for filename in expected}
    if actual != expected:
        raise RuntimeError(f"{name}: reference source identity mismatch")
    return actual


def validate_compatibility_report(report, protocol, root):
    if report.get("status") != "PASS" or report.get("native_cuda") is not True:
        raise RuntimeError("Native equivalence evidence is required")
    if report.get("identity_verification_schema") != 2:
        raise RuntimeError("Compatibility report lacks verified reference identities")
    protocol_file = Path(root) / "configs/resubmission/protocol.json"
    if report.get("protocol_sha256") != sha256_file(protocol_file):
        raise RuntimeError("Compatibility report predates this protocol")
    expected = protocol["expected_reference_sha256"]
    if report.get("reference_sha256") != expected["historical_9a80bf6"]:
        raise RuntimeError(
            "Historical reference hashes do not match the frozen protocol"
        )
    if report.get("qh_reference_sha256") != expected["archival_qh_20260916"]:
        raise RuntimeError("Q/H reference hashes do not match the original snapshot")
    current = report.get("source_sha256", {})
    if set(current) != set(MODEL_SOURCE_FILES):
        raise RuntimeError("Current model/factory identity is incomplete")
    if current != {name: sha256_file(Path(root) / name) for name in MODEL_SOURCE_FILES}:
        raise RuntimeError("Compatibility report predates model/factory changes")

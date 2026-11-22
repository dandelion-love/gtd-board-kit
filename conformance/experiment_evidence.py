"""Reference selection and receipt checks for experiment evidence discovery."""
import hashlib
import json
import re
from datetime import datetime

HEX = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")

def digest(value):
    return hashlib.sha256(value).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def answer(case):
    """Select exactly one line, validate its evidence envelope; never fetch or replay."""
    try:
        target = case["result_line_sha256"]
        if not HEX.fullmatch(target) or not COMMIT.fullmatch(case["ref"]):
            raise ValueError("identity")
        if "source_text" in case:
            source = case["source_text"]
            if case["layout"] == "jsonl":
                lines = [line[:-1] if line.endswith("\r") else line
                         for line in source.split("\n")]
            elif case["layout"] == "page":
                lines = re.findall(r"(?m)^```json record\r?\n([^\r\n]+)\r?\n```\r?$", source)
            else:
                raise ValueError("unsupported-layout")
        else:
            lines = case["lines"]
        matches = [line for line in lines if digest(line.encode("utf-8")) == target]
        if len(matches) != 1:
            raise ValueError("missing-or-duplicate")
        rec = json.loads(matches[0])
        if rec.get("id") != case["id"] or rec.get("event") != "result":
            raise ValueError("wrong-result")
        data = rec.get("data")
        if rec.get("verdict", "").upper() == "VOID" and not data:
            status, envelope = "empty-void", None
        elif not isinstance(data, dict) or "review_evidence" not in data:
            status, envelope = "legacy", None
        else:
            status, envelope = "present", data["review_evidence"]
            if not isinstance(envelope, dict) or set(envelope) != {"receipt", "receipt_sha256"}:
                raise ValueError("invalid-envelope")
            receipt = envelope["receipt"]
            required = {"version", "method", "uri", "generation", "bundle_sha256", "manifest_sha256", "replay_sha256", "result_sha256", "verified_at"}
            if not isinstance(receipt, dict) or set(receipt) != required or receipt["version"] != 1 or receipt["method"] != "immutable-bundle-local-python-replay-v1":
                raise ValueError("invalid-receipt")
            for field in ("bundle_sha256", "manifest_sha256", "replay_sha256", "result_sha256"):
                if not isinstance(receipt[field], str) or not HEX.fullmatch(receipt[field]):
                    raise ValueError("invalid-digest")
            uri, generation = receipt["uri"], receipt["generation"]
            gcs = isinstance(uri, str) and re.fullmatch(r"gs://[a-z0-9][a-z0-9._-]{1,220}/[A-Za-z0-9._~/-]+", uri) and isinstance(generation, str) and re.fullmatch(r"[1-9][0-9]*", generation)
            git = isinstance(uri, str) and re.fullmatch(r"git:[A-Za-z0-9_./-]+", uri) and ".." not in uri[4:].split("/") and isinstance(generation, str) and COMMIT.fullmatch(generation)
            if not (gcs or git):
                raise ValueError("invalid-source")
            if not isinstance(receipt["verified_at"], str):
                raise ValueError("invalid-timestamp")
            timestamp = datetime.fromisoformat(receipt["verified_at"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None or digest(canonical(receipt)) != envelope["receipt_sha256"]:
                raise ValueError("invalid-receipt-hash")
            payload = {k: v for k, v in data.items() if k != "review_evidence"}
            if digest(canonical(payload)) != receipt["result_sha256"]:
                raise ValueError("invalid-result-hash")
        return {"evidence_status": status, "verdict": rec.get("verdict"), "result_data": data, "review_evidence": envelope}
    except (KeyError, ValueError, TypeError, OverflowError, json.JSONDecodeError):
        return {"error": "refused"}

if __name__ == "__main__":
    import sys
    print(json.dumps(answer(json.load(sys.stdin)), ensure_ascii=False))

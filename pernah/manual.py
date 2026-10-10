from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .manual_input import capture_text
from .storage import Storage



def _serialize_capture(captured):
    draft = captured["draft"]
    return {
        "intent": draft.intent,
        "detected_language": draft.detected_language,
        "source_type": draft.source_type,
        "confidence": draft.confidence,
        "occurred_at": draft.occurred_at,
        "result": captured["result"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="PERNAH manual input: capture one text input into local canonical storage."
    )
    parser.add_argument("--db", default="pernah.db", help="SQLite database path (default: pernah.db)")
    parser.add_argument("--text", help="text to capture; omit for interactive input")
    parser.add_argument(
        "--reference-time",
        help="ISO-8601 reference timestamp used for relative-time normalization",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="print machine-readable result")
    args = parser.parse_args(argv)

    text = args.text
    if text is None:
        try:
            text = input("PERNAH > ")
        except EOFError:
            parser.error("no input text supplied")

    reference_time = None
    if args.reference_time:
        try:
            reference_time = datetime.fromisoformat(args.reference_time.replace("Z", "+00:00"))
        except ValueError as exc:
            parser.error(f"invalid --reference-time: {exc}")

    with Storage(Path(args.db)) as db:
        captured = capture_text(db, text, reference_time=reference_time)
        if args.as_json:
            print(json.dumps(_serialize_capture(captured), ensure_ascii=False, sort_keys=True))
        else:
            draft = captured["draft"]
            result = captured["result"]
            print(f"Captured: {draft.intent}")
            print(f"Memory ID: {result['memory_id']}")
            if draft.occurred_at:
                print(f"Occurred at: {draft.occurred_at}")
            if draft.entities:
                print("Entities: " + ", ".join(e["name"] for e in draft.entities))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

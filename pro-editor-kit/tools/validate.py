#!/usr/bin/env python3
"""validate — check a brief / scene plan / sfx library against pro-editor-kit/schemas.

Small built-in JSON-Schema subset (type, required, properties, items, enum,
minimum, maximum, minItems, additionalProperties=false) so no pip install is needed.

  python3 validate.py brief.json --schema brief
  python3 validate.py scene-plan.json --schema scene-plan
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_json  # noqa: E402

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def check(value, schema, where="$"):
    errs = []
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        ok = False
        for ty in types:
            if ty == "number":
                ok |= isinstance(value, (int, float)) and not isinstance(value, bool)
            elif ty == "integer":
                ok |= isinstance(value, int) and not isinstance(value, bool)
            else:
                ok |= isinstance(value, TYPES[ty])
        if not ok:
            return [f"{where}: expected {t}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{where}: {value!r} not in {schema['enum']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{where}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{where}: {value} > maximum {schema['maximum']}")
    if isinstance(value, dict):
        for r in schema.get("required", []):
            if r not in value:
                errs.append(f"{where}: missing required '{r}'")
        props = schema.get("properties", {})
        for k, v in value.items():
            if k in props:
                errs += check(v, props[k], f"{where}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{where}: unexpected property '{k}'")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errs.append(f"{where}: needs >= {schema['minItems']} items")
        if "items" in schema:
            for i, v in enumerate(value):
                errs += check(v, schema["items"], f"{where}[{i}]")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--schema", required=True, help="brief | scene-plan | sfx-library | qa-report, or a path")
    a = ap.parse_args(argv)
    sp = Path(a.schema)
    if not sp.exists():
        sp = SCHEMAS / f"{a.schema}.schema.json"
    errs = check(load_json(a.file), load_json(sp))
    for e in errs:
        print("invalid:", e)
    print(f"validate: {'OK' if not errs else str(len(errs)) + ' problem(s)'} ({a.file} vs {sp.name})")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate catalog shape and cross-record invariants without depending on the CLI."""

import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def normalize(value):
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def main():
    schema = json.loads(
        (ROOT / "schema/component.schema.json").read_text(encoding="utf-8")
    )
    records = {}
    for file in sorted((ROOT / "database").glob("*.json")):
        data = json.loads(file.read_text(encoding="utf-8"), object_pairs_hook=unique)
        jsonschema.validate(data, schema)
        duplicates = records.keys() & data.keys()
        if duplicates:
            raise ValueError(f"duplicate component IDs: {duplicates}")
        records.update(data)
    if not records:
        raise ValueError("database is empty")
    tokens = {}
    for key in records:
        token = normalize(key)
        if token in tokens:
            raise ValueError(f"ambiguous normalized ID: {key}")
        tokens[token] = key
    for key, record in records.items():
        numbers = [str(pin["number"]) for pin in record["pins"]]
        if len(numbers) != len(set(numbers)):
            raise ValueError(f"{key}: duplicate pin numbers")
        layout = record["layout"]
        if layout["type"] == "dip" and len(numbers) % 2:
            raise ValueError(f"{key}: odd number of pins in DIP layout")
        if layout["type"] in {"dual", "header"}:
            used = [n for row in layout["rows"] for n in row if n is not None]
            if sorted(used) != sorted(numbers):
                raise ValueError(f"{key}: layout must include every pin exactly once")
        for alias in record.get("aliases", []):
            token = normalize(alias)
            if not token or (token in tokens and tokens[token] != key):
                raise ValueError(f"{key}: ambiguous alias {alias!r}")
            tokens[token] = key
    print(f"Valid: {len(records)} package-specific components")


if __name__ == "__main__":
    main()

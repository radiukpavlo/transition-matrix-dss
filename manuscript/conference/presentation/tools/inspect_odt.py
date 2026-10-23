from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def xml_text(blob: bytes) -> str:
    try:
        root = ET.fromstring(blob)
    except ET.ParseError:
        return ""
    parts: list[str] = []
    for node in root.iter():
        if node.text:
            parts.append(node.text)
        if node.tail:
            parts.append(node.tail)
    return clean(" ".join(parts))


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: inspect_odt.py input.odt extracted.json output.txt", file=sys.stderr)
        return 2

    odt_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    data = json.loads(json_path.read_text(encoding="utf-8"))

    lines: list[str] = []
    lines.append("# Headings")
    for index, heading in enumerate(data["headings"], 1):
        lines.append(f"{index}. L{heading.get('level')} {heading['text']}")

    lines.append("\n# Captions")
    for paragraph in data["paragraphs"]:
        if re.match(r"^(Fig\\.|Figure|Table)\\s", paragraph):
            lines.append(paragraph)

    lines.append("\n# Tables")
    for index, table in enumerate(data["tables"], 1):
        rows = table["rows"]
        width = max(len(row) for row in rows)
        lines.append(f"Table object {index}: {table.get('name')} ({len(rows)} x {width})")
        for row in rows[:12]:
            lines.append(" | ".join(row))
        if len(rows) > 12:
            lines.append("...")
        lines.append("")

    lines.append("\n# Figures")
    for index, figure in enumerate(data["figures"], 1):
        lines.append(f"{index}. {figure['href']}")

    lines.append("\n# Equations")
    with zipfile.ZipFile(odt_path) as archive:
        for name in data["equation_objects"]:
            lines.append(f"## {name}")
            lines.append(xml_text(archive.read(name)) or "(no plain text)")

    lines.append("\n# First Paragraphs")
    for paragraph in data["paragraphs"][:40]:
        lines.append(paragraph)

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

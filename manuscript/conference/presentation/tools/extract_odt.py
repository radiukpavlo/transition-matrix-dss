from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def element_text(element: ET.Element) -> str:
    parts: list[str] = []
    for child in element.iter():
        tag = child.tag.rsplit("}", 1)[-1]
        if child.text:
            parts.append(child.text)
        if tag == "tab":
            parts.append("\t")
        if tag in {"line-break", "soft-page-break"}:
            parts.append("\n")
        if child.tail:
            parts.append(child.tail)
    return clean_text("".join(parts))


def table_rows(table: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.findall("table:table-row", NS):
        repeated_rows = int(row.attrib.get(f"{{{NS['table']}}}number-rows-repeated", "1"))
        parsed_row: list[str] = []
        for cell in row.findall("table:table-cell", NS):
            repeated_cols = int(cell.attrib.get(f"{{{NS['table']}}}number-columns-repeated", "1"))
            cell_text = element_text(cell)
            parsed_row.extend([cell_text] * min(repeated_cols, 8))
        if any(parsed_row):
            for _ in range(min(repeated_rows, 8)):
                rows.append(parsed_row)
    return rows


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: extract_odt.py input.odt output.json", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    with zipfile.ZipFile(input_path) as archive:
        content = archive.read("content.xml")
        embedded = archive.namelist()

    root = ET.fromstring(content)
    items: list[dict[str, object]] = []
    headings: list[dict[str, object]] = []
    paragraphs: list[str] = []
    figures: list[dict[str, str]] = []
    tables: list[dict[str, object]] = []

    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "h":
            text = element_text(element)
            if text:
                level = element.attrib.get(f"{{{NS['text']}}}outline-level", "")
                item = {"type": "heading", "level": level, "text": text}
                items.append(item)
                headings.append(item)
        elif tag == "p":
            text = element_text(element)
            if text:
                style = element.attrib.get(f"{{{NS['text']}}}style-name", "")
                item = {"type": "paragraph", "style": style, "text": text}
                items.append(item)
                paragraphs.append(text)
        elif tag == "table":
            name = element.attrib.get(f"{{{NS['table']}}}name", "")
            rows = table_rows(element)
            if rows:
                item = {"type": "table", "name": name, "rows": rows}
                items.append(item)
                tables.append(item)
        elif tag == "image":
            href = element.attrib.get(f"{{{NS['xlink']}}}href", "")
            if href:
                figures.append({"href": href})
                items.append({"type": "image", "href": href})

    equations = []
    for name in embedded:
        if name.startswith("Object ") and name.endswith("content.xml"):
            equations.append(name)

    output_path.write_text(
        json.dumps(
            {
                "headings": headings,
                "paragraphs": paragraphs,
                "figures": figures,
                "tables": tables,
                "equation_objects": equations,
                "items": items,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"wrote {output_path}")
    print(f"headings={len(headings)} paragraphs={len(paragraphs)} tables={len(tables)} figures={len(figures)} equations={len(equations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

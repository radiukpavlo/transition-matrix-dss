from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: export_odt_items.py extracted.json output.txt", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    lines: list[str] = []
    paragraph_index = 0
    table_index = 0
    figure_index = 0
    for item in data["items"]:
        item_type = item["type"]
        if item_type == "heading":
            lines.append("")
            lines.append(f"## H{item.get('level')} {item['text']}")
        elif item_type == "paragraph":
            paragraph_index += 1
            lines.append(f"P{paragraph_index:03d}: {item['text']}")
        elif item_type == "table":
            table_index += 1
            lines.append(f"T{table_index:02d}: {item.get('name')} ({len(item['rows'])} rows)")
        elif item_type == "image":
            figure_index += 1
            lines.append(f"I{figure_index:02d}: {item['href']}")
    Path(sys.argv[2]).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

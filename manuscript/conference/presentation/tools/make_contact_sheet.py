from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_contact_sheet.py render_dir output.png", file=sys.stderr)
        return 2
    render_dir = Path(sys.argv[1])
    output = Path(sys.argv[2])
    paths = sorted(render_dir.glob("page-*.png"))
    if not paths:
        print("no page images found", file=sys.stderr)
        return 1

    thumbs = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((360, 203))
        canvas = Image.new("RGB", (380, 235), "white")
        x = (360 - image.width) // 2 + 10
        canvas.paste(image, (x, 10))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 214), path.stem.replace("page-", "Slide "), fill=(20, 20, 20))
        thumbs.append(canvas)

    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 380, rows * 235), "white")
    for index, thumb in enumerate(thumbs):
        x = (index % cols) * 380
        y = (index // cols) * 235
        sheet.paste(thumb, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

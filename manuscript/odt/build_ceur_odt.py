from __future__ import annotations

import datetime as dt
import posixpath
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
ODT_DIR = ROOT / "manuscript" / "odt"
WORK_DIR = ODT_DIR / "_conversion_work" / "85_Paper_v0.3"
TEMPLATE = ODT_DIR / "ceur-template-1col-icyberphys_2026.odt"
OUTPUT = ODT_DIR / "85_Paper_v0.3_ceur_formatted.odt"
MEDIA_DIR = ODT_DIR / "_conversion_work" / "generated_media"
POPPLER = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "poppler" / "Library" / "bin" / "pdftoppm.exe"


NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "manifest": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
    "dc": "http://purl.org/dc/elements/1.1/",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(name: str) -> str:
    prefix, local = name.split(":", 1)
    return f"{{{NS[prefix]}}}{local}"


def el(name: str, attrs: dict[str, str] | None = None, text: str | None = None) -> ET.Element:
    node = ET.Element(q(name))
    if attrs:
        for key, value in attrs.items():
            node.set(q(key) if ":" in key else key, value)
    if text is not None:
        node.text = text
    return node


def append_text(node: ET.Element, text: str) -> None:
    if not text:
        return
    if len(node):
        last = node[-1]
        last.tail = (last.tail or "") + text
    else:
        node.text = (node.text or "") + text


def append_text_with_breaks(node: ET.Element, text: str) -> None:
    parts = text.split("\n")
    for index, part in enumerate(parts):
        if index:
            node.append(el("text:line-break"))
        append_text(node, part)


def plain_p(style: str, text: str = "") -> ET.Element:
    p = el("text:p", {"text:style-name": style})
    append_inlines(p, text)
    return p


def heading(style: str, level: int, text: str) -> ET.Element:
    h = el("text:h", {"text:style-name": style, "text:outline-level": str(level)})
    append_inlines(h, text)
    return h


def text_span(style: str, text: str) -> ET.Element:
    span = el("text:span", {"text:style-name": style})
    append_text_with_breaks(span, text)
    return span


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def block_between(source: str, begin: str, end: str) -> str:
    pattern = re.escape(begin) + r"(.*?)" + re.escape(end)
    match = re.search(pattern, source, flags=re.S)
    return match.group(1).strip() if match else ""


def command_arg(source: str, command: str) -> str:
    start = source.find("\\" + command)
    if start < 0:
        return ""
    brace = source.find("{", start)
    if brace < 0:
        return ""
    value, _ = find_braced(source, brace)
    return value


def strip_comments(source: str) -> str:
    rows = []
    for line in source.splitlines():
        if line.lstrip().startswith("%%"):
            continue
        rows.append(re.sub(r"(?<!\\)%.*$", "", line).rstrip())
    return "\n".join(rows)


def latex_accents(text: str) -> str:
    replacements = {
        r"{\'i}": "i",
        r"{\'I}": "I",
        r"{\'a}": "a",
        r"{\'e}": "e",
        r"{\'o}": "o",
        r"{\'u}": "u",
        r"{\'n}": "n",
        r"{\'D}": "D",
        r"{\'\i}": "i",
        r"{\"u}": "u",
        r"{\"o}": "o",
        r"{\"O}": "O",
        r"{\`o}": "o",
        r"{\`i}": "i",
        r"{\c{S}}": "S",
        r"{\l}": "l",
        r"\l": "l",
        r"\'i": "i",
        r"\'a": "a",
        r"\'e": "e",
        r"\'o": "o",
        r"\"u": "u",
        r"\`o": "o",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def parse_bibliography(bbl: str, tex_source: str) -> tuple[dict[str, int], list[str]]:
    entries: list[tuple[str, str]] = []
    for chunk in re.split(r"\\bibitem", bbl)[1:]:
        key_match = re.search(r"\]\{([^}]+)\}", chunk)
        if not key_match:
            key_match = re.search(r"\{([^}]+)\}", chunk)
        if not key_match:
            continue
        key = key_match.group(1)
        start = key_match.end()
        body = chunk[start:]
        entries.append((key, clean_reference(body)))
    cited_keys: list[str] = []
    for cite_group in re.findall(r"\\cite\{([^}]+)\}", tex_source):
        for key in cite_group.split(","):
            key = key.strip()
            if key and key not in cited_keys:
                cited_keys.append(key)
    present = {key for key, _ in entries}
    missing_refs = {
        "Musaelian2023Allegro": "A. Musaelian, S. Batzner, A. Johansson, L. Sun, C. J. Owen, M. Kornbluth, B. Kozinsky, Learning local equivariant representations for large-scale atomistic dynamics, Nat. Commun. 14 (2023) 579. doi:10.1038/s41467-023-36329-y."
    }
    for missing in [key for key in cited_keys if key not in present and key in missing_refs]:
        insert_at = len(entries)
        if missing == "Musaelian2023Allegro":
            for index, (key, _) in enumerate(entries):
                if key == "Radiuk2026EquivariantTransition":
                    insert_at = index + 1
                    break
        entries.insert(insert_at, (missing, missing_refs[missing]))
    cite_numbers = {key: index + 1 for index, (key, _) in enumerate(entries)}
    return cite_numbers, [body for _, body in entries]


def unwrap_command(text: str, command: str) -> str:
    pattern = re.compile(r"\\" + re.escape(command) + r"\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(lambda m: m.group(1), text)
    return text


def clean_reference(text: str) -> str:
    text = re.sub(r"\\ifx.*", "", text)
    text = re.sub(r"%Type\s*=.*", "", text)
    text = text.replace(r"\newblock", " ")
    text = re.sub(r"\\bibinfo\{[^}]+\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", lambda m: m.group(1), text)
    text = re.sub(r"\\href\{[^}]+\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", lambda m: m.group(1), text)
    text = re.sub(r"\\doi\{([^}]+)\}", lambda m: m.group(1), text)
    text = re.sub(r"\\url\{([^}]+)\}", lambda m: m.group(1), text)
    text = text.replace(r"\DOIprefix", " doi:")
    text = text.replace(r"\URLprefix", " URL: ")
    text = unwrap_command(text, "emph")
    text = unwrap_command(text, "textit")
    text = unwrap_command(text, "textbf")
    text = latex_to_text(text, {}, {}, {}, {}, math_mode=False)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_braced(source: str, start: int) -> tuple[str, int]:
    if source[start] != "{":
        raise ValueError("expected opening brace")
    depth = 0
    for index in range(start, len(source)):
        char = source[index]
        if char == "{" and (index == 0 or source[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or source[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return source[start + 1 : index], index + 1
    raise ValueError("unclosed brace")


def latex_math_to_text(text: str) -> str:
    text = text.strip()
    replacements = {
        r"\mathbb{R}": "\u211d",
        r"\times": "\u00d7",
        r"\lambda": "\u03bb",
        r"\sigma": "\u03c3",
        r"\theta": "\u03b8",
        r"\widetilde": "",
        r"\left": "",
        r"\right": "",
        r"\in": "\u2208",
        r"\pm": "\u00b1",
        r"\geq": "\u2265",
        r"\leq": "\u2264",
        r"\wedge": "\u2227",
        r"\bigwedge": "\u22c0",
        r"\Rightarrow": "\u21d2",
        r"\mathrm": "",
        r"\mathcal": "",
        r"\_": "_",
        r"\%": "%",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]+\])?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("^", "^").replace("_", "_")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def latex_to_text(
    text: str,
    cite_numbers: dict[str, int],
    fig_numbers: dict[str, int],
    table_numbers: dict[str, int],
    eq_numbers: dict[str, int],
    *,
    math_mode: bool = False,
) -> str:
    if math_mode:
        return latex_math_to_text(text)
    text = text.replace("\r", "")
    text = text.replace("~", " ")
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace("---", "-").replace("--", "-")
    text = text.replace(r"\&", "&").replace(r"\%", "%").replace(r"\_", "_")
    text = text.replace(r"\,", ",").replace(r"\;", ";")
    text = re.sub(r"\\cite\{([^}]+)\}", lambda m: cite_text(m.group(1), cite_numbers), text)
    text = re.sub(r"\\eqref\{([^}]+)\}", lambda m: f"({eq_numbers.get(m.group(1), '?')})", text)
    text = re.sub(r"\\ref\{([^}]+)\}", lambda m: ref_text(m.group(1), fig_numbers, table_numbers, eq_numbers), text)
    text = re.sub(r"\\url\{([^}]+)\}", lambda m: m.group(1), text)
    text = re.sub(r"\$([^$]+)\$", lambda m: latex_math_to_text(m.group(1)), text)
    text = re.sub(r"\\mathrm\{([^{}]+)\}", lambda m: m.group(1), text)
    text = re.sub(r"\\texttt\{([^{}]+)\}", lambda m: m.group(1), text)
    text = re.sub(r"\\makecell(?:\[[^\]]+\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", lambda m: m.group(1), text)
    text = text.replace(r"\\", "\n")
    text = text.replace(r"\addlinespace", "")
    text = text.replace(r"\toprule", "").replace(r"\midrule", "").replace(r"\bottomrule", "")
    text = text.replace(r"\sep", ";")
    text = latex_accents(text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]+\])?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("$", "")
    text = text.replace("Uuditing fidelity", "Auditing fidelity")
    text = text.replace("large language models LLMs", "large language models (LLMs)")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def cite_text(keys: str, cite_numbers: dict[str, int]) -> str:
    values = []
    for key in [part.strip() for part in keys.split(",")]:
        values.append(str(cite_numbers.get(key, "?")))
    return "[" + ", ".join(values) + "]"


def ref_text(
    key: str,
    fig_numbers: dict[str, int],
    table_numbers: dict[str, int],
    eq_numbers: dict[str, int],
) -> str:
    if key in fig_numbers:
        return str(fig_numbers[key])
    if key in table_numbers:
        return str(table_numbers[key])
    if key in eq_numbers:
        return str(eq_numbers[key])
    if key.startswith("sec:"):
        return section_numbers.get(key, "?")
    if key.startswith("subsec:"):
        return subsection_numbers.get(key, "?")
    return "?"


section_numbers: dict[str, str] = {}
subsection_numbers: dict[str, str] = {}


def inline_fragment(text: str) -> str:
    if not text:
        return ""
    leading = " " if text[:1].isspace() else ""
    trailing = " " if text[-1:].isspace() else ""
    cleaned = latex_to_text(text, {}, {}, {}, {})
    if not cleaned:
        return " " if leading or trailing else ""
    return leading + cleaned + trailing


def append_inlines(parent: ET.Element, text: str) -> None:
    pattern = re.compile(r"(\\textbf\{|\\emph\{|\\textit\{|\$)")
    index = 0
    while index < len(text):
        match = pattern.search(text, index)
        if not match:
            append_text_with_breaks(parent, inline_fragment(text[index:]))
            break
        append_text_with_breaks(parent, inline_fragment(text[index : match.start()]))
        token = match.group(1)
        if token == "$":
            end = text.find("$", match.end())
            if end == -1:
                append_text(parent, "$")
                index = match.end()
                continue
            math = latex_math_to_text(text[match.end() : end])
            parent.append(text_span("TM_MathInline", math))
            index = end + 1
            continue
        content_start = match.end()
        try:
            content, new_index = find_braced("{" + text[content_start:], 0)
        except ValueError:
            append_text(parent, token)
            index = match.end()
            continue
        style = "TM_Strong" if token.startswith(r"\textbf") else "TM_Emph"
        parent.append(text_span(style, latex_to_text(content, {}, {}, {}, {})))
        index = content_start + len(content) + 1


def add_custom_styles(auto_styles: ET.Element) -> None:
    def add_style(name: str, family: str, parent: str | None = None) -> ET.Element:
        style = el("style:style", {"style:name": name, "style:family": family})
        if parent:
            style.set(q("style:parent-style-name"), parent)
        auto_styles.append(style)
        return style

    strong = add_style("TM_Strong", "text")
    strong.append(el("style:text-properties", {"fo:font-weight": "bold", "style:font-weight-asian": "bold", "style:font-weight-complex": "bold"}))
    emph = add_style("TM_Emph", "text")
    emph.append(el("style:text-properties", {"fo:font-style": "italic", "style:font-style-asian": "italic", "style:font-style-complex": "italic"}))
    math_inline = add_style("TM_MathInline", "text")
    math_inline.append(el("style:text-properties", {"style:font-name": "Cambria Math", "fo:font-size": "10pt"}))
    sup = add_style("TM_Sup", "text")
    sup.append(el("style:text-properties", {"style:text-position": "super 58%", "fo:font-size": "58%"}))

    table_text = add_style("TM_TableText", "paragraph", "Standard")
    table_text.append(el("style:paragraph-properties", {"fo:margin-top": "0cm", "fo:margin-bottom": "0cm", "fo:text-indent": "0cm"}))
    table_text.append(el("style:text-properties", {"fo:font-size": "8pt"}))
    table_head = add_style("TM_TableHead", "paragraph", "Standard")
    table_head.append(el("style:paragraph-properties", {"fo:margin-top": "0cm", "fo:margin-bottom": "0cm", "fo:text-align": "center"}))
    table_head.append(el("style:text-properties", {"fo:font-size": "8pt", "fo:font-weight": "bold"}))
    page_break = add_style("TM_PageBreak", "paragraph", "Standard")
    page_break.append(el("style:paragraph-properties", {"fo:break-before": "page"}))

    for name, attrs in {
        "TM_CellHeader": {
            "fo:padding-left": "0.08cm",
            "fo:padding-right": "0.08cm",
            "fo:padding-top": "0.04cm",
            "fo:padding-bottom": "0.04cm",
            "fo:border-left": "none",
            "fo:border-right": "none",
            "fo:border-top": "1.5pt solid #000000",
            "fo:border-bottom": "0.75pt solid #000000",
            "style:vertical-align": "middle",
        },
        "TM_CellBody": {
            "fo:padding-left": "0.08cm",
            "fo:padding-right": "0.08cm",
            "fo:padding-top": "0.04cm",
            "fo:padding-bottom": "0.04cm",
            "fo:border": "none",
            "style:vertical-align": "middle",
        },
        "TM_CellBottom": {
            "fo:padding-left": "0.08cm",
            "fo:padding-right": "0.08cm",
            "fo:padding-top": "0.04cm",
            "fo:padding-bottom": "0.04cm",
            "fo:border-left": "none",
            "fo:border-right": "none",
            "fo:border-top": "none",
            "fo:border-bottom": "1.5pt solid #000000",
            "style:vertical-align": "middle",
        },
        "TM_EqCell": {
            "fo:padding-left": "0cm",
            "fo:padding-right": "0cm",
            "fo:padding-top": "0.05cm",
            "fo:padding-bottom": "0.05cm",
            "fo:border": "none",
            "style:vertical-align": "middle",
        },
    }.items():
        style = add_style(name, "table-cell")
        style.append(el("style:table-cell-properties", attrs))


def convert_figure(pdf_name: str, out_name: str) -> Path:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    pdf = WORK_DIR / "figures" / pdf_name
    prefix = MEDIA_DIR / out_name.removesuffix(".png")
    subprocess.run([str(POPPLER), "-png", "-r", "180", "-singlefile", str(pdf), str(prefix)], check=True)
    return prefix.with_suffix(".png")


def combine_images(left: Path, right: Path, out_name: str) -> Path:
    with Image.open(left) as img_l, Image.open(right) as img_r:
        img_l = img_l.convert("RGB")
        img_r = img_r.convert("RGB")
        target_h = max(img_l.height, img_r.height)
        def scale(img: Image.Image) -> Image.Image:
            ratio = target_h / img.height
            return img.resize((int(img.width * ratio), target_h))
        img_l = scale(img_l)
        img_r = scale(img_r)
        gap = 50
        label_h = 34
        combined = Image.new("RGB", (img_l.width + img_r.width + gap, target_h + label_h), "white")
        combined.paste(img_l, (0, label_h))
        combined.paste(img_r, (img_l.width + gap, label_h))
        draw = ImageDraw.Draw(combined)
        draw.text((8, 8), "(a)", fill="black")
        draw.text((img_l.width + gap + 8, 8), "(b)", fill="black")
        out = MEDIA_DIR / out_name
        combined.save(out, optimize=True)
        return out


def image_frame(image_href: str, width_cm: float, image_path: Path, name: str) -> ET.Element:
    with Image.open(image_path) as im:
        ratio = im.height / im.width
    height_cm = width_cm * ratio
    para = el("text:p", {"text:style-name": "P22"})
    frame = el(
        "draw:frame",
        {
            "draw:name": name,
            "text:anchor-type": "as-char",
            "svg:width": f"{width_cm:.2f}cm",
            "svg:height": f"{height_cm:.2f}cm",
            "draw:z-index": "0",
        },
    )
    frame.append(el("draw:image", {"xlink:href": image_href, "xlink:type": "simple", "xlink:show": "embed", "xlink:actuate": "onLoad"}))
    para.append(frame)
    return para


def collect_labels(source: str) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    fig_numbers: dict[str, int] = {}
    table_numbers: dict[str, int] = {}
    eq_numbers: dict[str, int] = {}
    for index, match in enumerate(re.finditer(r"\\begin\{figure\}(.*?)\\end\{figure\}", source, flags=re.S), start=1):
        for label in re.finditer(r"\\label\{([^}]+)\}", match.group(1)):
            fig_numbers[label.group(1)] = index
    for index, match in enumerate(re.finditer(r"\\begin\{table\}(.*?)\\end\{table\}", source, flags=re.S), start=1):
        label = re.search(r"\\label\{([^}]+)\}", match.group(1))
        if label:
            table_numbers[label.group(1)] = index
    for index, match in enumerate(re.finditer(r"\\begin\{equation\}(.*?)\\end\{equation\}", source, flags=re.S), start=1):
        label = re.search(r"\\label\{([^}]+)\}", match.group(1))
        if label:
            eq_numbers[label.group(1)] = index
    sec_index = 0
    sub_index = 0
    for line in source.splitlines():
        sec = re.match(r"\\section\{(.+?)\}\\label\{([^}]+)\}", line)
        if sec:
            sec_index += 1
            sub_index = 0
            section_numbers[sec.group(2)] = str(sec_index)
        sub = re.match(r"\\subsection\{(.+?)\}\\label\{([^}]+)\}", line)
        if sub:
            sub_index += 1
            subsection_numbers[sub.group(2)] = f"{sec_index}.{sub_index}"
    return fig_numbers, table_numbers, eq_numbers


def split_rows(body: str) -> list[str]:
    rows: list[str] = []
    start = 0
    depth = 0
    index = 0
    while index < len(body) - 1:
        char = body[index]
        if char == "{" and (index == 0 or body[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or body[index - 1] != "\\"):
            depth -= 1
        elif char == "\\" and body[index + 1] == "\\" and depth == 0:
            rows.append(body[start:index].strip())
            index += 2
            start = index
            continue
        index += 1
    tail = body[start:].strip()
    if tail:
        rows.append(tail)
    return rows


def split_cells(row: str) -> list[str]:
    cells: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(row):
        if char == "{" and (index == 0 or row[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or row[index - 1] != "\\"):
            depth -= 1
        elif char == "&" and depth == 0:
            cells.append(row[start:index].strip())
            start = index + 1
    cells.append(row[start:].strip())
    return cells


def parse_table_rows(block: str, cite_numbers, fig_numbers, table_numbers, eq_numbers) -> list[list[str]]:
    tabular = block_between(block, r"\begin{tabular}", r"\end{tabular}")
    if not tabular:
        return []
    if tabular.startswith("{"):
        _, after = find_braced(tabular, 0)
        tabular = tabular[after:]
    for rule in (r"\toprule", r"\midrule", r"\bottomrule", r"\addlinespace"):
        tabular = tabular.replace(rule, "")
    rows = []
    for row in split_rows(tabular):
        if not row.strip():
            continue
        cells = []
        for cell in split_cells(row):
            cleaned = latex_to_text(cell, cite_numbers, fig_numbers, table_numbers, eq_numbers)
            cleaned = re.sub(r"\s*\n\s*", "; ", cleaned)
            cleaned = re.sub(r";\s*;", ";", cleaned)
            cleaned = cleaned.replace("AND; ", "AND ")
            cells.append(cleaned)
        if cells:
            rows.append(cells)
    return rows


def table_widths(label: str, cols: int) -> list[float]:
    manual = {
        "tab:protocol_a_metrics": [2.2, 2.2, 2.2, 8.1],
        "tab:rulebook_properties": [4.4, 3.4, 3.4, 3.5],
        "tab:synthetic_stress_test": [2.4, 1.8, 2.7, 2.4, 2.3, 2.1],
        "tab:induced_production_rules": [1.4, 3.9, 4.2, 1.6, 1.4, 1.2],
        "tab:rule_inference_traces": [2.0, 1.1, 1.3, 1.2, 1.5, 1.0, 1.1, 1.0, 4.5],
    }
    if label in manual:
        return manual[label]
    return [14.7 / cols] * cols


def add_table_styles(auto_styles: ET.Element, name: str, widths: list[float]) -> None:
    table_style = el("style:style", {"style:name": name, "style:family": "table"})
    table_style.append(el("style:table-properties", {"style:width": f"{sum(widths):.3f}cm", "table:align": "center", "fo:margin-top": "0.05cm", "fo:margin-bottom": "0.25cm"}))
    auto_styles.append(table_style)
    for index, width in enumerate(widths):
        col_style = el("style:style", {"style:name": f"{name}.C{index+1}", "style:family": "table-column"})
        col_style.append(el("style:table-column-properties", {"style:column-width": f"{width:.3f}cm"}))
        auto_styles.append(col_style)


def make_table(name: str, label: str, caption: str, rows: list[list[str]], auto_styles: ET.Element) -> list[ET.Element]:
    if not rows:
        return [plain_p("P10", "[Table omitted: unable to parse source table.]")]
    widths = table_widths(label, len(rows[0]))
    add_table_styles(auto_styles, name, widths)
    nodes = []
    if label == "tab:induced_production_rules":
        nodes.append(plain_p("TM_PageBreak", ""))
    nodes.append(plain_p("P25", caption))
    table = el("table:table", {"table:name": name, "table:style-name": name})
    for idx in range(len(rows[0])):
        table.append(el("table:table-column", {"table:style-name": f"{name}.C{idx+1}"}))
    for r_index, row in enumerate(rows):
        tr = el("table:table-row")
        for cell in row:
            style = "TM_CellHeader" if r_index == 0 else ("TM_CellBottom" if r_index == len(rows) - 1 else "TM_CellBody")
            tc = el("table:table-cell", {"table:style-name": style, "office:value-type": "string"})
            pstyle = "TM_TableHead" if r_index == 0 else "TM_TableText"
            para = el("text:p", {"text:style-name": pstyle})
            append_text_with_breaks(para, cell)
            tc.append(para)
            tr.append(tc)
        table.append(tr)
    nodes.append(table)
    return nodes


def make_list(items: list[str], ordered: bool, cite_numbers, fig_numbers, table_numbers, eq_numbers) -> ET.Element:
    list_style = "WWNum3" if ordered else "WWNum4"
    pstyle = "P13" if ordered else "P19"
    lst = el("text:list", {"text:style-name": list_style})
    for item in items:
        list_item = el("text:list-item")
        para = el("text:p", {"text:style-name": pstyle})
        append_inlines(para, latex_to_text(item, cite_numbers, fig_numbers, table_numbers, eq_numbers))
        list_item.append(para)
        lst.append(list_item)
    return lst


def make_equation(eq_text: str, number: int, auto_styles: ET.Element) -> ET.Element:
    name = f"TM_Equation_{number}"
    if not any(style.get(q("style:name")) == name for style in auto_styles.findall(q("style:style"))):
        add_table_styles(auto_styles, name, [13.4, 1.3])
    table = el("table:table", {"table:name": name, "table:style-name": name})
    table.append(el("table:table-column", {"table:style-name": f"{name}.C1"}))
    table.append(el("table:table-column", {"table:style-name": f"{name}.C2"}))
    tr = el("table:table-row")
    left = el("table:table-cell", {"table:style-name": "TM_EqCell", "office:value-type": "string"})
    p_left = el("text:p", {"text:style-name": "P24"})
    append_text(p_left, latex_math_to_text(re.sub(r"\\label\{[^}]+\}", "", eq_text)))
    left.append(p_left)
    right = el("table:table-cell", {"table:style-name": "TM_EqCell", "office:value-type": "string"})
    p_right = el("text:p", {"text:style-name": "P26"})
    append_text(p_right, f"({number})")
    right.append(p_right)
    tr.extend([left, right])
    table.append(tr)
    return table


def parse_items(block: str) -> list[str]:
    items = []
    current: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]") and not current:
            continue
        if stripped.startswith(r"\item"):
            if current:
                items.append(" ".join(current).strip())
            current = [stripped[len(r"\item") :].strip()]
        elif stripped:
            current.append(stripped)
    if current:
        items.append(" ".join(current).strip())
    return items


def build_body(source: str, bbl: str, auto_styles: ET.Element) -> list[ET.Element]:
    cite_numbers, refs = parse_bibliography(bbl, source)
    fig_numbers, table_numbers, eq_numbers = collect_labels(source)

    title = re.search(r"\\title\{(.+?)\}", source, flags=re.S).group(1)
    conference = re.search(r"\\conference\{(.+?)\}", source, flags=re.S).group(1)
    copyright_clause = re.search(r"\\copyrightclause\{(.+?)\}", source, flags=re.S).group(1)
    abstract = block_between(source, r"\begin{abstract}", r"\end{abstract}")
    keywords = block_between(source, r"\begin{keywords}", r"\end{keywords}")

    nodes: list[ET.Element] = []
    nodes.append(plain_p("P2", latex_to_text(conference, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
    nodes.append(plain_p("P1", latex_to_text(title, cite_numbers, fig_numbers, table_numbers, eq_numbers)))

    author_p = el("text:p", {"text:style-name": "P3"})
    authors = [
        ("Pavlo Radiuk", "1"),
        ("Oleksander Barmak", "1"),
        ("Iurii Krak", "2,3"),
    ]
    for index, (name, aff) in enumerate(authors):
        if index:
            append_text(author_p, ", " if index < len(authors) - 1 else " and ")
        append_text(author_p, name)
        author_p.append(text_span("TM_Sup", aff))
    nodes.append(author_p)
    nodes.append(plain_p("P4", "1. Department of Computer Science, Khmelnytskyi National University, 11 Instytuts'ka Str., 29016 Khmelnytskyi, Ukraine"))
    nodes.append(plain_p("P4", "2. Department of Theoretical Cybernetics, Taras Shevchenko National University of Kyiv, 4d Akademika Glushkova Ave, 03680 Kyiv, Ukraine"))
    nodes.append(plain_p("P4", "3. Laboratory of Communicative Information Technologies, V.M. Glushkov Institute of Cybernetics, 40 Akademika Glushkova Ave, 03187 Kyiv, Ukraine"))
    nodes.append(plain_p("P6", "Corresponding author: Pavlo Radiuk, radiukp@khmnu.edu.ua."))
    nodes.append(plain_p("P8", latex_to_text(copyright_clause, cite_numbers, fig_numbers, table_numbers, eq_numbers)))

    abstract_p = el("text:p", {"text:style-name": "P10"})
    abstract_p.append(text_span("TM_Strong", "Abstract. "))
    append_inlines(abstract_p, latex_to_text(abstract, cite_numbers, fig_numbers, table_numbers, eq_numbers))
    nodes.append(abstract_p)
    keywords_p = el("text:p", {"text:style-name": "P10"})
    keywords_p.append(text_span("TM_Strong", "Keywords: "))
    append_inlines(keywords_p, latex_to_text(keywords, cite_numbers, fig_numbers, table_numbers, eq_numbers))
    nodes.append(keywords_p)

    content = source.split(r"\maketitle", 1)[1].split(r"\bibliography", 1)[0]
    tokens = list(re.finditer(r"\\begin\{(?:figure|table|equation|itemize|enumerate)\}|\\section\*?\{|\\subsection\{", content))
    cursor = 0
    fig_counter = 0
    table_counter = 0
    eq_counter = 0
    table_auto_index = 0

    def add_paragraphs(fragment: str) -> None:
        buffer: list[str] = []
        for raw in fragment.splitlines():
            stripped = raw.strip()
            if not stripped or stripped.startswith("%"):
                if buffer:
                    text = " ".join(buffer).strip()
                    if text:
                        nodes.append(plain_p("P10", latex_to_text(text, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
                    buffer.clear()
                continue
            buffer.append(stripped)
        if buffer:
            text = " ".join(buffer).strip()
            if text:
                nodes.append(plain_p("P10", latex_to_text(text, cite_numbers, fig_numbers, table_numbers, eq_numbers)))

    for token in tokens:
        add_paragraphs(content[cursor : token.start()])
        marker = token.group(0)
        if marker.startswith(r"\section"):
            braced, end = find_braced(content, token.end() - 1)
            if marker.startswith(r"\section*"):
                nodes.append(heading("P28", 1, latex_to_text(braced, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
            else:
                nodes.append(heading("P9", 1, latex_to_text(braced, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
            label = re.match(r"\\label\{[^}]+\}", content[end:].lstrip())
            cursor = end + (label.end() if label else 0)
        elif marker.startswith(r"\subsection"):
            braced, end = find_braced(content, token.end() - 1)
            nodes.append(heading("P12", 2, latex_to_text(braced, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
            label = re.match(r"\\label\{[^}]+\}", content[end:].lstrip())
            cursor = end + (label.end() if label else 0)
        else:
            env = re.match(r"\\begin\{([^}]+)\}", marker).group(1)
            end_marker = rf"\end{{{env}}}"
            end_pos = content.find(end_marker, token.end())
            block = content[token.end() : end_pos]
            cursor = end_pos + len(end_marker)
            if env == "figure":
                fig_counter += 1
                caption = command_arg(block, "caption")
                includes = re.findall(r"\\includegraphics(?:\[[^\]]+\])?\{([^}]+)\}", block)
                media_name = f"figure_{fig_counter}.png"
                if len(includes) == 2:
                    left = convert_figure(includes[0], f"figure_{fig_counter}a.png")
                    right = convert_figure(includes[1], f"figure_{fig_counter}b.png")
                    image_path = combine_images(left, right, media_name)
                    width = 14.2
                else:
                    image_path = convert_figure(includes[0], media_name)
                    width = 14.0 if ".65" not in block and ".72" not in block else (9.7 if ".65" in block else 10.7)
                href = f"Pictures/{media_name}"
                nodes.append(image_frame(href, width, image_path, f"Figure {fig_counter}"))
                nodes.append(plain_p("P22", f"Figure {fig_counter}: " + latex_to_text(caption, cite_numbers, fig_numbers, table_numbers, eq_numbers)))
            elif env == "table":
                table_counter += 1
                label_match = re.search(r"\\label\{([^}]+)\}", block)
                label = label_match.group(1) if label_match else f"table-{table_counter}"
                caption = f"Table {table_counter}: " + latex_to_text(command_arg(block, "caption"), cite_numbers, fig_numbers, table_numbers, eq_numbers)
                rows = parse_table_rows(block, cite_numbers, fig_numbers, table_numbers, eq_numbers)
                table_auto_index += 1
                nodes.extend(make_table(f"TM_Table_{table_auto_index}", label, caption, rows, auto_styles))
                note_match = re.search(r"\\begin\{flushleft\}\\footnotesize\s*(.*?)\\end\{flushleft\}", block, flags=re.S)
                if note_match:
                    nodes.append(plain_p("P6", latex_to_text(note_match.group(1), cite_numbers, fig_numbers, table_numbers, eq_numbers)))
            elif env == "equation":
                eq_counter += 1
                nodes.append(make_equation(block, eq_counter, auto_styles))
            elif env in ("itemize", "enumerate"):
                nodes.append(make_list(parse_items(block), env == "enumerate", cite_numbers, fig_numbers, table_numbers, eq_numbers))

    add_paragraphs(content[cursor:])

    nodes.append(heading("P33", 1, "References"))
    ref_list = el("text:list", {"text:style-name": "WWNum24"})
    for ref in refs:
        item = el("text:list-item")
        item.append(plain_p("P34", ref))
        ref_list.append(item)
    nodes.append(ref_list)
    return nodes


def update_meta(meta_bytes: bytes, title: str) -> bytes:
    root = ET.fromstring(meta_bytes)
    title_node = root.find(".//" + q("dc:title"))
    if title_node is None:
        meta_el = root.find(q("office:meta"))
        if meta_el is not None:
            title_node = el("dc:title")
            meta_el.insert(0, title_node)
    if title_node is not None:
        title_node.text = title
    date_node = root.find(".//" + q("meta:editing-cycles"))
    if date_node is not None:
        date_node.text = "1"
    gen = root.find(".//" + q("meta:generator"))
    if gen is not None:
        gen.text = "Codex ODT builder using CEUR LibreOffice template"
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def update_manifest(manifest_bytes: bytes, picture_names: list[str]) -> bytes:
    root = ET.fromstring(manifest_bytes)
    existing = {entry.get(q("manifest:full-path")) for entry in root.findall(q("manifest:file-entry"))}
    for picture in picture_names:
        full_path = f"Pictures/{picture}"
        if full_path not in existing:
            root.append(el("manifest:file-entry", {"manifest:full-path": full_path, "manifest:media-type": "image/png"}))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_odt(content_bytes: bytes, meta_bytes: bytes, manifest_bytes: bytes, picture_paths: list[Path]) -> None:
    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        with zipfile.ZipFile(OUTPUT, "w") as zout:
            mimetype = zin.read("mimetype")
            zout.writestr("mimetype", mimetype, compress_type=zipfile.ZIP_STORED)
            for info in zin.infolist():
                if info.filename in {"mimetype", "content.xml", "meta.xml", "META-INF/manifest.xml"}:
                    continue
                zout.writestr(info, zin.read(info.filename))
            zout.writestr("content.xml", content_bytes, compress_type=zipfile.ZIP_DEFLATED)
            zout.writestr("meta.xml", meta_bytes, compress_type=zipfile.ZIP_DEFLATED)
            zout.writestr("META-INF/manifest.xml", manifest_bytes, compress_type=zipfile.ZIP_DEFLATED)
            for picture in picture_paths:
                zout.write(picture, posixpath.join("Pictures", picture.name), compress_type=zipfile.ZIP_DEFLATED)


def main() -> None:
    if MEDIA_DIR.exists():
        shutil.rmtree(MEDIA_DIR)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    tex = strip_comments(read_text(WORK_DIR / "main.tex"))
    bbl = read_text(WORK_DIR / "main.bbl")
    title = re.search(r"\\title\{(.+?)\}", tex, flags=re.S).group(1)

    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        content_root = ET.fromstring(zin.read("content.xml"))
        meta_bytes = zin.read("meta.xml")
        manifest_bytes = zin.read("META-INF/manifest.xml")

    auto_styles = content_root.find(q("office:automatic-styles"))
    if auto_styles is None:
        raise RuntimeError("template has no automatic styles")
    add_custom_styles(auto_styles)
    office_text = content_root.find(".//" + q("office:text"))
    if office_text is None:
        raise RuntimeError("template has no office:text body")
    for child in list(office_text):
        office_text.remove(child)
    for node in build_body(tex, bbl, auto_styles):
        office_text.append(node)

    content_bytes = ET.tostring(content_root, encoding="utf-8", xml_declaration=True)
    picture_paths = sorted(MEDIA_DIR.glob("figure_*.png"))
    manifest_updated = update_manifest(manifest_bytes, [p.name for p in picture_paths])
    meta_updated = update_meta(meta_bytes, latex_to_text(title, {}, {}, {}, {}))
    write_odt(content_bytes, meta_updated, manifest_updated, picture_paths)
    print(OUTPUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Read an .ods or .xlsx into rows of strings, with the standard library only.

WHY THIS EXISTS. Two of the ten national short registers are published as a
spreadsheet and nothing else: Sweden's Finansinspektionen serves
`GetBlankningsregisterAggregat` as an OpenDocument sheet and CONSOB serves
`PncPubbl.xlsx`. This container has no `openpyxl`, no `odfpy` and no `pandas`, and
`pip install` is not part of a Routine's job -- the same constraint that made
`eu_pdftext.py` necessary for the AMF's PDFs.

Both formats are a zip of XML, so both are readable without a dependency. What this
module does NOT do is evaluate formulas, read styles or preserve types: every cell
comes back as the string the file displays. That is the right shape here, because a
register row is an issuer name, an ISIN, a percentage and a date, and every one of
those is parsed by the caller anyway.

THE TWO TRAPS, both of which cost a parse before they were handled:

  ODS repeats cells by ATTRIBUTE. `<table:table-cell table:number-columns-repeated="8"/>`
  is eight empty cells, not one, and a naive parse shifts every column after it. The
  same attribute is used to pad every row out to the sheet width, so it also has to be
  capped or a 1024-column pad turns one row into a megabyte of empty strings.

  XLSX stores strings OUT OF LINE and addresses cells SPARSELY. A cell holds an index
  into `xl/sharedStrings.xml` when `t="s"`, and a row simply omits the cells that are
  empty -- so `<c r="C5">` after `<c r="A5">` means B5 is blank and the column has to be
  recovered from the `r` reference rather than from position.
"""
import re
import zipfile
import xml.etree.ElementTree as ET

# An ODS row padded to the sheet width can claim thousands of repeats. Cap it: no
# register has a thousand real columns, and honouring the pad makes the row unusable.
MAX_REPEAT = 256


def _col_index(ref):
    """`BC12` -> 54. The letters are base-26 with no zero, which is why this is a loop."""
    letters = re.match(r"([A-Z]+)", ref or "")
    if not letters:
        return 0
    n = 0
    for ch in letters.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(data, sheet=1):
    """Rows of strings from an .xlsx given as bytes. `sheet` is 1-based."""
    z = zipfile.ZipFile(data if hasattr(data, "read") else __import__("io").BytesIO(data))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root:
            # A string can be split across several <t> runs by formatting; join them.
            shared.append("".join(t.text or "" for t in si.iter()
                                  if t.tag.endswith("}t")))
    name = f"xl/worksheets/sheet{sheet}.xml"
    if name not in z.namelist():
        return []
    root = ET.fromstring(z.read(name))
    out = []
    for row in root.iter():
        if not row.tag.endswith("}row"):
            continue
        cells = {}
        for c in row:
            if not c.tag.endswith("}c"):
                continue
            idx = _col_index(c.get("r", ""))
            typ = c.get("t")
            val = ""
            for kid in c:
                if kid.tag.endswith("}v"):
                    val = kid.text or ""
                elif kid.tag.endswith("}is"):
                    val = "".join(t.text or "" for t in kid.iter()
                                  if t.tag.endswith("}t"))
            if typ == "s" and val.isdigit() and int(val) < len(shared):
                val = shared[int(val)]
            cells[idx] = val
        out.append(["" if i not in cells else cells[i]
                    for i in range(max(cells) + 1)] if cells else [])
    return out


def read_ods(data, sheet=1):
    """Rows of strings from an .ods given as bytes. `sheet` is 1-based."""
    z = zipfile.ZipFile(data if hasattr(data, "read") else __import__("io").BytesIO(data))
    root = ET.fromstring(z.read("content.xml"))
    tables = [e for e in root.iter() if e.tag.endswith("}table")]
    if len(tables) < sheet:
        return []
    out = []
    for row in tables[sheet - 1]:
        if not row.tag.endswith("}table-row"):
            continue
        vals = []
        for c in row:
            if not c.tag.endswith("}table-cell"):
                continue
            txt = "".join(t.text or "" for t in c.iter() if t.tag.endswith("}p")
                          or t.tag.endswith("}span"))
            # The repeat attribute is namespaced; the prefix is not guaranteed, so
            # match on the local name.
            rep = 1
            for k, v in c.attrib.items():
                if k.endswith("}number-columns-repeated"):
                    try:
                        rep = min(int(v), MAX_REPEAT)
                    except ValueError:
                        rep = 1
            vals.extend([txt.strip()] * rep)
        # Trailing pad is noise; drop it so a row's length means something.
        while vals and not vals[-1]:
            vals.pop()
        out.append(vals)
    return out


def read(data, sheet=1):
    """Sniff the format off the zip's own contents rather than off a filename."""
    import io
    buf = data if hasattr(data, "read") else io.BytesIO(data)
    names = zipfile.ZipFile(buf).namelist()
    buf.seek(0) if hasattr(buf, "seek") else None
    return (read_ods(buf, sheet) if "content.xml" in names
            else read_xlsx(buf, sheet))

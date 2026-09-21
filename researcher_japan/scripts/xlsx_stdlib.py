"""Minimal read-only .xlsx row reader on the standard library alone.

An .xlsx is a zip of XML. openpyxl is not installed in the container stage J fires
into and nothing in this repo declares it, so the JPX cohort sheets are unreadable
there. This yields the same shape `openpyxl`'s `iter_rows(values_only=True)` does
for the columns jp_universe reads: a tuple per row, with date cells as `datetime`.
"""
import re, zipfile, io
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
BUILTIN_DATE = set(range(14, 23)) | set(range(45, 48)) | {27, 30, 36, 50, 57}


def _col(ref):
    m = re.match(r"([A-Z]+)", ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _serial(v):
    # Excel's 1900 epoch, with its deliberate leap-year bug for serials >= 60.
    return datetime(1899, 12, 30) + timedelta(days=float(v))


def rows(blob):
    z = zipfile.ZipFile(io.BytesIO(blob))

    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")):
            shared.append("".join(t.text or "" for t in si.iter(NS + "t")))

    date_styles = set()
    if "xl/styles.xml" in z.namelist():
        st = ET.fromstring(z.read("xl/styles.xml"))
        custom = {int(n.get("numFmtId")): (n.get("formatCode") or "")
                  for n in st.iter(NS + "numFmt")}
        xfs = st.find(NS + "cellXfs")
        for i, xf in enumerate(xfs or []):
            fid = int(xf.get("numFmtId") or 0)
            code = custom.get(fid, "")
            if fid in BUILTIN_DATE or re.search(r"[yYdD]", re.sub(r"\[[^\]]*\]|\"[^\"]*\"", "", code)):
                date_styles.add(i)

    name = next((n for n in ("xl/worksheets/sheet1.xml",) if n in z.namelist()), None)
    if name is None:
        name = sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet"))[0]

    out, width = [], 0
    for row in ET.fromstring(z.read(name)).iter(NS + "row"):
        cells = {}
        for c in row.iter(NS + "c"):
            t, s = c.get("t"), c.get("s")
            v = c.find(NS + "v")
            if t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(NS + "t"))
            elif v is None or v.text is None:
                val = None
            elif t == "s":
                val = shared[int(v.text)]
            elif t in ("str", "e"):
                val = v.text
            else:
                try:
                    num = float(v.text)
                except ValueError:
                    val = v.text
                else:
                    val = _serial(num) if (s is not None and int(s) in date_styles) else (
                        int(num) if num.is_integer() else num)
            cells[_col(c.get("r"))] = val
        width = max(width, (max(cells) + 1) if cells else 0)
        out.append(cells)
    # openpyxl pads every row to the sheet width; callers index fixed columns and
    # an IndexError on a short row is not the same thing as an empty cell.
    return [tuple(c.get(i) for i in range(width)) for c in out]

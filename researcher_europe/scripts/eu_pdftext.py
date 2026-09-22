#!/usr/bin/env python3
"""Text out of a PDF, with nothing but the standard library.

WHY THIS EXISTS
---------------
The primary documents in this stage are PDFs. The AMF's regulated-information flux --
which is France's RNS and the best confirmation source in this stage -- links every
filing as a PDF, and a threshold-crossing declaration or a `Communique sur comptes,
resultats` exists in no other form. So does BALO, and so do most German filings.

And this container cannot read them any other way. Measured 2026-09-19:

  pdftotext          not installed
  pdfminer.six       ImportError: the `cryptography` package raises
                     `ModuleNotFoundError: No module named '_cffi_backend'` and then a
                     pyo3 PanicException, so anything importing it dies
  pypdf              same failure, same cause -- it imports cryptography for its crypt
                     providers
  WebFetch on a PDF  returns "corrupted or improperly encoded ... garbled binary data",
                     twice, on two different AMF PDFs

That left the hunt reading a French 5% threshold declaration through a search snippet,
which is exactly the "a number you could not confirm in the document is not
load-bearing" case the hunters are told to refuse.

WHAT IT DOES AND WHAT IT DOES NOT
----------------------------------
It inflates every FlateDecode stream in the file and pulls the literal strings out of
the text-showing operators. That is enough to read a press release or a regulatory
declaration and to quote it. It is NOT a layout engine: inter-character spacing inside
a word is often lost or doubled (`D e c l a r a t i o n  d e  f r a n c h i s s e m e n t`),
tables come out as a run of numbers with no columns, and a PDF whose text is an image
returns nothing at all. Normalise whitespace before quoting, and **quote what the
document says, not what this script's spacing suggests**.

  python3 researcher_europe/scripts/eu_pdftext.py <file.pdf> [max_chars]
  curl -sSL -o /tmp/f.pdf "<url>" && python3 .../eu_pdftext.py /tmp/f.pdf 4000
"""
import re
import sys
import zlib

_STRING = re.compile(rb"\((?:\\.|[^\\()])*\)")
_ESCAPE = re.compile(rb"\\([nrtbf()\\])")
_ESCAPES = {b"n": b"\n", b"r": b"\n", b"t": b"\t", b"b": b"", b"f": b"\n"}


_HEX = re.compile(rb"<([0-9A-Fa-f\s]*)>")
_BFCHAR = re.compile(rb"beginbfchar(.*?)endbfchar", re.S)
_BFRANGE = re.compile(rb"beginbfrange(.*?)endbfrange", re.S)
_PAIR = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")
_TRIPLE = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")


def _utf16_be(h):
    """A ToUnicode destination is UTF-16BE, possibly several code points."""
    try:
        return bytes.fromhex(h.decode("ascii")).decode("utf-16-be", "replace")
    except Exception:
        return ""


def _parse_cmap(stream):
    """One ToUnicode CMap -> {code: text}. Codes are the font's own byte values."""
    cmap = {}
    for blk in _BFCHAR.findall(stream):
        for src, dst in _PAIR.findall(blk):
            cmap[int(src, 16)] = _utf16_be(dst)
    for blk in _BFRANGE.findall(stream):
        for lo, hi, dst in _TRIPLE.findall(blk):
            lo_i, hi_i = int(lo, 16), int(hi, 16)
            if hi_i - lo_i > 65535:
                continue
            base = _utf16_be(dst)
            for k in range(lo_i, hi_i + 1):
                # A bfrange destination increments its LAST code unit across the range.
                cmap[k] = (base[:-1] + chr(ord(base[-1]) + k - lo_i)) if base else ""
    return cmap


def _streams(data):
    """Every stream in the file, decompressed where it is Flate."""
    for m in re.finditer(rb"stream\r?\n", data):
        st = m.end()
        en = data.find(b"endstream", st)
        if en < 0:
            continue
        raw = data[st:en]
        try:
            yield zlib.decompress(raw)
        except Exception:
            yield raw                     # uncompressed, or an image/font we skip


_OBJ = re.compile(rb"(\d+)\s+0\s+obj(.*?)endobj", re.S)
_TOUNI = re.compile(rb"/ToUnicode\s+(\d+)\s+0\s+R")
_FONTRES = re.compile(rb"/Font\s*<<(.*?)>>", re.S)
_FONTREF = re.compile(rb"/([A-Za-z0-9_.+-]+)\s+(\d+)\s+0\s+R")
_TF = re.compile(rb"/([A-Za-z0-9_.+-]+)\s+[\d.]+\s+Tf")


def _objects(data):
    """{object number: body}. Plain `N 0 obj ... endobj` only, which is what the
    French AMF and Italian issuer PDFs use; objects inside an object stream are not
    reached and their fonts simply resolve to no CMap."""
    return {int(n): body for n, body in _OBJ.findall(data)}


def _obj_stream(data, body):
    """The decompressed stream belonging to one object body."""
    m = re.search(rb"stream\r?\n", body)
    if not m:
        return None
    en = body.find(b"endstream", m.end())
    raw = body[m.end():en if en >= 0 else len(body)]
    try:
        return zlib.decompress(raw)
    except Exception:
        return raw


def _font_cmaps(data):
    """{resource name (e.g. b"F1"): {code: text}}, resolved PER FONT.

    Merging every ToUnicode CMap in a document into one table does NOT work, and the
    failure is silent corruption rather than an error: subset fonts renumber their
    glyphs from 1, so two fonts both use code 34 for different letters. Measured
    2026-09-22 on a French AMF filing, a merged table rendered "Relations" as
    "ReelatilWoWns" -- readable enough to quote and wrong.
    """
    objs = _objects(data)
    uni = {}
    for num, body in objs.items():
        m = _TOUNI.search(body)
        if m:
            tgt = int(m.group(1))
            if tgt in objs:
                st = _obj_stream(data, objs[tgt])
                if st and (b"beginbfchar" in st or b"beginbfrange" in st):
                    uni[num] = _parse_cmap(st)
    out = {}
    for body in objs.values():
        for res in _FONTRES.findall(body):
            for name, ref in _FONTREF.findall(res):
                if int(ref) in uni:
                    out[name] = uni[int(ref)]
    return out


def _decode_hex(tok, cmap):
    h = re.sub(rb"\s", b"", tok[1:-1])
    if len(h) % 4 == 0 and len(h) > 0:
        codes = [int(h[i:i + 4], 16) for i in range(0, len(h), 4)]
        if cmap and all(c in cmap for c in codes):
            return "".join(cmap[c] for c in codes)
    codes = [int(h[i:i + 2], 16) for i in range(0, len(h) - len(h) % 2, 2)]
    return "".join(cmap.get(c, "") for c in codes)


def extract(path_or_bytes):
    """Text from a PDF, including the HEX-encoded and subset-font kinds.

    Three encodings reach a content stream and this repo used to read only the first.
    A `(literal)` string is plain text in a standard font. In a SUBSET font -- which is
    what an issuer's design software emits for its headline figures -- both `(literal)`
    and `<hex>` strings carry the font's OWN renumbered codes, which mean nothing until
    they are mapped through that font's ToUnicode CMap.

    MEASURED 2026-09-22 on an Italian issuer release: every headline euro figure was set
    in a bold subset font and emitted as hex, so the old extractor returned fluent
    English prose with the numbers missing -- "Net Profit for the period of ___
    thousand" -- and reported success. A blank where a number should be is worse than a
    failure, because nothing downstream can tell the two apart.

    CMaps are resolved PER FONT, by following `/Font << /F1 N 0 R >>` to that object's
    `/ToUnicode`, and the active font is tracked through `Tf` operators. Merging them
    into one table corrupts text silently instead (see `_font_cmaps`).
    """
    data = (path_or_bytes if isinstance(path_or_bytes, (bytes, bytearray))
            else open(path_or_bytes, "rb").read())
    fonts = _font_cmaps(data)
    fallback = {}
    if not fonts:                         # objects unreachable (object streams): merge
        for st in _streams(data):
            if b"beginbfchar" in st or b"beginbfrange" in st:
                fallback.update(_parse_cmap(st))

    out = []
    for st in _streams(data):
        if b"beginbfchar" in st or b"beginbfrange" in st:
            continue                      # a CMap is not page text
        cmap, toks = fallback, []
        for t in re.finditer(
                rb"/[A-Za-z0-9_.+-]+\s+[\d.]+\s+Tf"
                rb"|\((?:\\.|[^\\()])*\)"
                rb"|<[0-9A-Fa-f\s]*>", st):
            tok = t.group(0)
            if tok.endswith(b"Tf"):
                cmap = fonts.get(_TF.match(tok).group(1), fallback)
            elif tok.startswith(b"("):
                raw = _ESCAPE.sub(lambda x: _ESCAPES.get(x.group(1), x.group(1)),
                                  tok[1:-1])
                # In a subset font the literal bytes ARE font codes. Map them when this
                # font has a CMap that covers them; otherwise they are ordinary text.
                if cmap and raw and all(c in cmap for c in raw):
                    toks.append("".join(cmap[c] for c in raw))
                else:
                    toks.append(raw.decode("latin-1", "replace"))
            elif cmap:
                toks.append(_decode_hex(tok, cmap))
        if any(toks):
            out.append(" ".join(toks))
    return "\n".join(out)


def squeeze(text):
    """Collapse the spacing this extractor mangles, for reading rather than quoting."""
    return re.sub(r"[ \t]{2,}", " ", text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    print(squeeze(extract(sys.argv[1]))[:n])

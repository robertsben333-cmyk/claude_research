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


def extract(path_or_bytes):
    data = (path_or_bytes if isinstance(path_or_bytes, (bytes, bytearray))
            else open(path_or_bytes, "rb").read())
    out = []
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        try:
            s = zlib.decompress(data[start:end])
        except Exception:
            continue                      # image, font or uncompressed stream
        toks = [_ESCAPE.sub(lambda x: _ESCAPES.get(x.group(1), x.group(1)),
                            t.group(0)[1:-1])
                for t in _STRING.finditer(s)]
        if toks:
            out.append(b" ".join(toks))
    return b"\n".join(out).decode("latin-1", "replace")


def squeeze(text):
    """Collapse the spacing this extractor mangles, for reading rather than quoting."""
    return re.sub(r"[ \t]{2,}", " ", text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    print(squeeze(extract(sys.argv[1]))[:n])

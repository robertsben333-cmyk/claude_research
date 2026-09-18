#!/usr/bin/env python3
"""Serve the dashboard and make its refresh button real.

A file:// page cannot run a shell script. What it CAN do is talk to a server that is
already running, so this one answers two routes and both are usable from a page opened
straight off the disk:

    GET  /ping      "yes, a rebuilder is here" -- the page probes this on load and
                    turns its button live when it answers
    POST /rebuild   run the ledger and the renderer, return what they printed

    python3 dashboard/scripts/serve.py [--port 8765] [--offline]
    ./dashboard/update.sh --serve        # foreground
    ./dashboard/update.sh --serve-bg     # detached, shell back

Binds to 127.0.0.1, so only something already on this machine can reach it. Both
routes carry CORS headers for `null` (a file:// page) and localhost origins only: a
random site you happen to visit can still fire the POST -- it is a simple request --
but cannot read the answer. The rebuild re-reads data and rewrites two files, reads
the broker and never sends an order, so that is an acceptable worst case for a
server you start when you want it. Pass --token to require one anyway.
"""
import argparse
import json
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "dashboard"
LOCK = threading.Lock()


ALLOWED_ORIGIN = ("null",)


def cors_origin(origin):
    """`null` is what a file:// page sends. Localhost is the served copy. Anything
    else gets no header, so it cannot read what comes back."""
    if not origin or origin in ALLOWED_ORIGIN:
        return "null"
    if origin.startswith("http://127.0.0.1") or origin.startswith("http://localhost"):
        return origin
    return None


def make_handler(offline, token=None):
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(HERE), **kw)

        def log_message(self, fmt, *args):
            sys.stderr.write("  %s\n" % (fmt % args))

        def do_GET(self):
            if self.path.split("?")[0].rstrip("/") == "/ping":
                self._json(200, {"ok": True, "service": "edge-performance",
                                 "busy": LOCK.locked(), "offline": bool(offline),
                                 "needs_token": bool(token)})
                return
            super().do_GET()

        def do_OPTIONS(self):
            self._json(204, None)

        def do_POST(self):
            if self.path.split("?")[0].rstrip("/") != "/rebuild":
                self.send_error(404)
                return
            if token and self.path.split("token=")[-1].split("&")[0] != token:
                self._json(403, {"ok": False, "log": "wrong or missing --token"})
                return
            if not LOCK.acquire(blocking=False):
                self._json(409, {"ok": False, "log": "a rebuild is already running"})
                return
            try:
                cmd = [sys.executable, "dashboard/scripts/build_ledger.py"]
                if offline:
                    cmd.append("--offline")
                out = []
                ok = True
                for c in (cmd, [sys.executable,
                                "dashboard/scripts/build_dashboard.py"]):
                    r = subprocess.run(c, cwd=ROOT, capture_output=True, text=True,
                                       timeout=3600)
                    out.append(r.stdout + r.stderr)
                    if r.returncode != 0:
                        ok = False
                        break
                self._json(200 if ok else 500, {"ok": ok, "log": "\n".join(out)})
            except Exception as exc:
                self._json(500, {"ok": False, "log": f"{type(exc).__name__}: {exc}"})
            finally:
                LOCK.release()

        def _json(self, code, body):
            raw = b"" if body is None else json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            if raw:
                self.wfile.write(raw)

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            allow = cors_origin(self.headers.get("Origin"))
            if allow:
                self.send_header("Access-Control-Allow-Origin", allow)
                self.send_header("Vary", "Origin")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            super().end_headers()
    return H


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--offline", action="store_true",
                    help="the button rebuilds without contacting the broker")
    ap.add_argument("--token", help="require ?token=... on /rebuild")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(a.offline, a.token))
    print(f"dashboard: http://127.0.0.1:{a.port}/dashboard.html")
    print("the refresh button now works -- in this served copy AND in the file you")
    print("already have open, which probes this server on load. ctrl-c to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()

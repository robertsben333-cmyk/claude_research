#!/usr/bin/env python3
"""Serve the dashboard and make its refresh button real.

A file:// page cannot run a shell script, so the button in the header falls back
to copying the command. Started through this server it does the thing instead:
POST /rebuild runs the ledger and the renderer and streams back what they printed.

    python3 edge/performance/scripts/serve.py [--port 8765] [--offline]
    ./edge/performance/update.sh --serve

Binds to localhost only. It runs two scripts in this repo and nothing else -- no
arguments from the request reach a shell, and the broker is only ever read.
"""
import argparse
import json
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "edge" / "performance"
LOCK = threading.Lock()


def make_handler(offline):
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(HERE), **kw)

        def log_message(self, fmt, *args):
            sys.stderr.write("  %s\n" % (fmt % args))

        def do_POST(self):
            if self.path.rstrip("/") != "/rebuild":
                self.send_error(404)
                return
            if not LOCK.acquire(blocking=False):
                self._json(409, {"ok": False, "log": "a rebuild is already running"})
                return
            try:
                cmd = [sys.executable, "edge/performance/scripts/build_ledger.py"]
                if offline:
                    cmd.append("--offline")
                out = []
                ok = True
                for c in (cmd, [sys.executable,
                                "edge/performance/scripts/build_dashboard.py"]):
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
            raw = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()
    return H


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--offline", action="store_true",
                    help="the button rebuilds without contacting the broker")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(a.offline))
    print(f"dashboard: http://127.0.0.1:{a.port}/dashboard.html")
    print("the refresh button in the page now rebuilds for real. ctrl-c to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()

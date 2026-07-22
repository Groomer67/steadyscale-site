#!/usr/bin/env python3
"""Local preview server with caching disabled.

Usage (from the repo root):  python3 _scripts/serve.py [port]

Same as `python -m http.server`, but sends `Cache-Control: no-store` so the
browser re-reads every page from disk on each click — no stale copies of
renamed or edited pages during copy iteration.
"""
import http.server
import os
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), NoCacheHandler) as srv:
        print(f"Serving site at http://localhost:{port} (cache disabled) — Ctrl+C to stop")
        srv.serve_forever()

"""Threaded http.server double of a Tandoor instance for tests and dry runs.

Run standalone: fake_tandoor.py --port 8099 --seed fixtures/seed.json
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

LOGIN_HTML = "<html><body><form>Login</form></body></html>"
COLLECTIONS = ("food", "unit", "keyword", "automation", "recipe")


class FakeTandoor:
    def __init__(self, seed: dict, token: str = "test-token"):
        self.token = token
        self.version = seed.get("version", "2.7.2")
        self.db = {c: copy.deepcopy(seed.get(c, [])) for c in COLLECTIONS}
        self.requests: list[dict] = []
        self.read_only = False  # writes answer 403
        self.redirect_to: str | None = None  # every request answers 301 to this URL
        self.html_everywhere = False  # every path answers 200 text/html
        self.canned: list[tuple[str, str, int, object]] = []  # (method, path substring, status, body), used once
        self._lock = threading.Lock()
        self._server: ThreadingHTTPServer | None = None

    # -- lifecycle ---------------------------------------------------------
    def start(self, port: int = 0) -> str:
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):  # silence
                pass

            def _serve(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                body = json.loads(raw) if raw else None
                status, ctype, payload, extra = fake.handle(self.command, self.path, dict(self.headers), body)
                data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                for k, v in extra.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _serve

        self._server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{self._server.server_address[1]}"

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None

    # -- request handling --------------------------------------------------
    def can(self, method: str, path_substr: str, status: int, body: object) -> None:
        self.canned.append((method, path_substr, status, body))

    def handle(self, method, raw_path, headers, body):
        parts = urlsplit(raw_path)
        path, query = parts.path, {k: v[-1] for k, v in parse_qs(parts.query).items()}
        with self._lock:
            self.requests.append({"method": method, "path": path, "query": query, "headers": headers, "body": body})
            if self.redirect_to:
                return 301, "text/plain", b"", {"Location": self.redirect_to}
            if self.html_everywhere or not path.endswith("/"):
                return 200, "text/html", LOGIN_HTML.encode(), {}
            idx = path.find("/api/")
            rest = path[idx + 5:] if idx >= 0 else ""
            if rest != "server-settings/current/":
                if headers.get("Authorization") != f"Bearer {self.token}":
                    return 401, "application/json", {"detail": "Authentication credentials were not provided."}, {}
                if self.read_only and method != "GET":
                    return 403, "application/json", {"detail": "You do not have permission to perform this action."}, {}
            for i, (m, sub, status, canned_body) in enumerate(self.canned):
                if m == method and sub in path:
                    del self.canned[i]
                    return status, "application/json", canned_body, {}
            return self.route(method, rest, query, body)

    def route(self, method, rest, query, body):
        if rest == "server-settings/current/":
            return 200, "application/json", {"version": self.version}, {}
        m = re.fullmatch(r"([a-z-]+)/(?:(\d+)/)?", rest)
        if not m or m.group(1) not in self.db:
            return 404, "application/json", {"detail": "Not found."}, {}
        coll, item_id = m.group(1), m.group(2)
        items = self.db[coll]
        if item_id is None and method == "GET":
            return self.list_items(coll, items, query)
        if item_id is None and method == "POST":
            return self.create(coll, body)
        found = next((i for i in items if i["id"] == int(item_id or 0)), None)
        if found is None:
            return 404, "application/json", {"detail": "Not found."}, {}
        if method == "GET":
            return 200, "application/json", found, {}
        return 405, "application/json", {"detail": "Method not allowed."}, {}

    def list_items(self, coll, items, query):
        cap = 100 if coll == "recipe" else 200
        size = min(int(query.get("page_size", 50)), cap)
        page = int(query.get("page", 1))
        chunk = items[(page - 1) * size: page * size]
        more = page * size < len(items)
        nxt = f"http://unreachable.invalid/api/{coll}/?page={page + 1}" if more else None
        return 200, "application/json", {"count": len(items), "next": nxt, "previous": None, "results": chunk}, {}

    def create(self, coll, body):
        items = self.db[coll]
        if coll in ("food", "unit", "keyword"):
            existing = next((i for i in items if i["name"] == body.get("name")), None)
            if existing:
                return 201, "application/json", existing, {}
        new = {**body, "id": max((i["id"] for i in items), default=0) + 1}
        items.append(new)
        return 201, "application/json", new, {}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8099)
    ap.add_argument("--seed", required=True)
    a = ap.parse_args()
    with open(a.seed, encoding="utf-8") as f:
        fake = FakeTandoor(json.load(f))
    print(fake.start(a.port), flush=True)
    threading.Event().wait()

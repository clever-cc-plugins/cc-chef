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
COLLECTIONS = ("food", "unit", "keyword", "automation", "recipe", "unit-conversion")


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
        self.recipe_mutator = None  # callable(recipe) run on every stored recipe, to simulate a lossy server
        self._tick = 0
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
            return self.create_recipe(body) if coll == "recipe" else self.create(coll, body)
        found = next((i for i in items if i["id"] == int(item_id or 0)), None)
        if found is None:
            return 404, "application/json", {"detail": "Not found."}, {}
        if method == "GET":
            return 200, "application/json", found, {}
        if method == "PATCH" and coll == "recipe":
            return self.patch_recipe(found, body)
        return 405, "application/json", {"detail": "Method not allowed."}, {}

    def list_items(self, coll, items, query):
        if query.get("query"):
            items = [i for i in items if query["query"].casefold() in i.get("name", "").casefold()]
        if query.get("extended") == "1" and coll in ("food", "unit"):
            items = [{**i, "numrecipe": i.get("numrecipe", self.recipes_using(coll, i["id"]))} for i in items]
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

    # -- recipes: nested writes like drf-writable-nested ---------------------
    def recipes_using(self, coll, item_id):
        return sum(
            any((ing.get(coll) or {}).get("id") == item_id for st in r["steps"] for ing in st["ingredients"])
            for r in self.db["recipe"]
        )

    def next_id(self, coll):
        return max((i["id"] for i in self.db[coll]), default=0) + 1

    def now(self):
        self._tick += 1
        return f"2026-11-05T10:00:00.{self._tick:06d}Z"

    def resolve_ref(self, coll, ref):
        """A nested object without id is get_or_create on the exact name; with id it updates that object from the payload."""
        items = self.db[coll]
        if ref.get("id") is not None:
            found = next((i for i in items if i["id"] == ref["id"]), None)
            if found is None:
                raise KeyError(f"{coll} {ref['id']}")
            if ref.get("name"):
                found["name"] = ref["name"]
            return {"id": found["id"], "name": found["name"]}
        found = next((i for i in items if i["name"] == ref.get("name")), None)
        if found is None:
            found = {"id": self.next_id(coll), "name": ref.get("name")}
            items.append(found)
        return {"id": found["id"], "name": found["name"]}

    def store_steps(self, steps):
        out, ing_id = [], max((i["id"] for r in self.db["recipe"] for s in r["steps"] for i in s["ingredients"]), default=0)
        step_id = max((s["id"] for r in self.db["recipe"] for s in r["steps"]), default=0)
        for step in steps:
            step_id += 1
            new = {**step, "id": step.get("id") or step_id, "ingredients": []}
            for ing in step.get("ingredients", []):
                ing_id += 1
                new["ingredients"].append({
                    **ing,
                    "id": ing.get("id") or ing_id,
                    "food": self.resolve_ref("food", ing["food"]),
                    "unit": self.resolve_ref("unit", ing["unit"]) if ing.get("unit") else None,
                })
            out.append(new)
        return out

    def create_recipe(self, body):
        rec = {**body, "id": self.next_id("recipe"), "created_at": self.now()}
        rec["updated_at"] = rec["created_at"]
        rec["steps"] = self.store_steps(body.get("steps", []))
        rec["keywords"] = [self.resolve_ref("keyword", k) for k in body.get("keywords", [])]
        if self.recipe_mutator:
            self.recipe_mutator(rec)
        self.db["recipe"].append(rec)
        return 201, "application/json", rec, {}

    def patch_recipe(self, found, body):
        for key, value in body.items():
            if key == "steps":  # steps left out are removed, steps without id are created
                found["steps"] = self.store_steps(value)
            elif key == "keywords":
                found["keywords"] = [self.resolve_ref("keyword", k) for k in value]
            else:
                found[key] = value
        found["updated_at"] = self.now()
        if self.recipe_mutator:
            self.recipe_mutator(found)
        return 200, "application/json", found, {}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8099)
    ap.add_argument("--seed", required=True)
    a = ap.parse_args()
    with open(a.seed, encoding="utf-8") as f:
        fake = FakeTandoor(json.load(f))
    print(fake.start(a.port), flush=True)
    threading.Event().wait()

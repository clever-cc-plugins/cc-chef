"""HTTP client for a Tandoor instance (standard library only).

Configuration comes only from TANDOOR_URL and TANDOOR_TOKEN. The token never
appears in a message: every error text goes through _scrub.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field


class TandoorError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class NotConfigured(TandoorError):
    pass


@dataclass(frozen=True)
class Config:
    url: str
    token: str = field(repr=False)


def load_config(env=os.environ) -> Config:
    url, token = (env.get("TANDOOR_URL") or "").strip(), (env.get("TANDOOR_TOKEN") or "").strip()
    if not url or not token:
        raise NotConfigured("Tandoor is not configured: set TANDOOR_URL and TANDOOR_TOKEN in the shell that starts Claude Code")
    return Config(url.rstrip("/"), token)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    # urllib would copy the Authorization header to the new host
    def redirect_request(self, *args, **kwargs):
        return None


class Client:
    def __init__(self, config: Config, timeout: int = 30):
        self.config = config
        self.timeout = timeout
        self._opener = urllib.request.build_opener(_NoRedirect)

    def _scrub(self, text: str) -> str:
        return text.replace(self.config.token, "***")

    def _fail(self, message: str, status: int | None = None) -> TandoorError:
        return TandoorError(self._scrub(message), status)

    def _request(self, method: str, path: str, params=None, body=None):
        url = f"{self.config.url}/{path.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.config.token}")
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with self._opener.open(req, timeout=self.timeout) as resp:
                raw, ctype = resp.read(), resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            try:
                raise self._http_error(e, method) from None
            finally:
                e.close()
        except (urllib.error.URLError, OSError) as e:
            reason = getattr(e, "reason", e)
            raise self._fail(f"cannot reach {self.config.url}: {reason}") from None
        if "html" in ctype.lower():
            raise self._fail(f"{self.config.url} answered with a web page, not the API: check TANDOOR_URL (path, scheme, trailing slash)")
        if not raw:
            return None
        try:
            return json.loads(raw)
        except ValueError:
            raise self._fail(f"{self.config.url} sent a response that is not JSON: check TANDOOR_URL") from None

    def _http_error(self, e: urllib.error.HTTPError, method: str) -> TandoorError:
        status = e.code
        if 300 <= status < 400:
            return self._fail(f"{self.config.url} redirects to {e.headers.get('Location', '?')}; not followed so the token stays on this host: fix TANDOOR_URL", status)
        if status == 401:
            return self._fail("the token was rejected (401): create a new one in Tandoor and set TANDOOR_TOKEN", status)
        if status == 403:
            hint = "the token needs the write scope" if method != "GET" else "the token lacks permission"
            return self._fail(f"forbidden (403): {hint}", status)
        detail = e.read().decode("utf-8", "replace")[:300]
        return self._fail(f"{method} failed ({status}): {detail}", status)

    def get(self, path, params=None):
        return self._request("GET", path, params)

    def post(self, path, body):
        return self._request("POST", path, body=body)

    def patch(self, path, body):
        return self._request("PATCH", path, body=body)

    def put(self, path, body=None):
        return self._request("PUT", path, body=body)

    def list_all(self, path, params=None, page_size=200):
        size = min(page_size, 100 if path.lstrip("/").startswith("api/recipe/") else 200)
        out: list[dict] = []
        page = 1
        while True:
            data = self.get(path, {**(params or {}), "page": page, "page_size": size})
            out.extend(data["results"])
            if not data.get("next"):
                return out  # never follow `next`: it can carry an internal host
            page += 1

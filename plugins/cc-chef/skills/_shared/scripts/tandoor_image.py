"""Download a recipe's source image so it can be attached to a Tandoor recipe (standard library only).

The URL comes from a web page, so it is untrusted: only http(s), only hosts that resolve to public
addresses (checked again on every redirect), a size cap and image content types. No credential is
ever sent; the Tandoor token is not known here.
"""
from __future__ import annotations

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request

from tandoor_client import TandoorError

MAX_BYTES = 10 * 1024 * 1024
TYPES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}


def check_scheme(url: str) -> None:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise TandoorError(f"image URL must start with http:// or https://: {url[:80]}")


def is_public_host(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return False
    return bool(infos) and all(ipaddress.ip_address(i[4][0].split("%")[0]).is_global for i in infos)


def _check(url: str) -> None:
    check_scheme(url)
    host = urllib.parse.urlsplit(url).hostname
    if not is_public_host(host):
        raise TandoorError(f"image host '{host}' is not a public address; not fetched")


class _CheckedRedirect(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _check(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, timeout: int = 30) -> tuple[bytes, str]:
    """Return (bytes, content type) of an image, or raise TandoorError."""
    _check(url)
    req = urllib.request.Request(url, headers={"User-Agent": "cc-chef", "Accept": "image/*"})
    try:
        with urllib.request.build_opener(_CheckedRedirect).open(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if ctype not in TYPES:
                raise TandoorError(f"the image URL sent '{ctype or 'no content type'}', not a jpeg, png, webp or gif image")
            data = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as e:
        raise TandoorError(f"image download failed ({e.code})") from None
    except (urllib.error.URLError, OSError) as e:
        raise TandoorError(f"image download failed: {getattr(e, 'reason', e)}") from None
    if len(data) > MAX_BYTES:
        raise TandoorError(f"the image is larger than {MAX_BYTES // (1024 * 1024)} MB")
    return data, ctype

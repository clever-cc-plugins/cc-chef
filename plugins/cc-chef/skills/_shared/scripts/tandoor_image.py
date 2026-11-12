"""Download a recipe's source image so it can be attached to a Tandoor recipe (standard library only).

The URL comes from a web page, so it is untrusted: only http(s), only hosts that resolve to public
addresses (checked again on every redirect, and the connection goes to the address that was checked, so a
second DNS answer cannot redirect it), a size cap and image content types. No credential is
ever sent; the Tandoor token is not known here.
"""
from __future__ import annotations

import http.client
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


def public_addresses(host: str, port: int = 0) -> list[str]:
    """Resolve host once; return its addresses, or [] when it has none or any of them is not public."""
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError:
        return []
    addresses = [i[4][0] for i in infos]
    return addresses if addresses and all(ipaddress.ip_address(a.split("%")[0]).is_global for a in addresses) else []


def _check(url: str) -> None:
    check_scheme(url)
    host = urllib.parse.urlsplit(url).hostname
    if not public_addresses(host):
        raise TandoorError(f"image host '{host}' is not a public address; not fetched")


def _connect_pinned(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    """Replacement for socket.create_connection: connect to the checked address, never to a second lookup."""
    host, port = address
    addresses = public_addresses(host, port)
    if not addresses:
        raise TandoorError(f"image host '{host}' is not a public address; not fetched")
    error = OSError(f"cannot connect to {host}")
    for ip in addresses:
        try:
            return socket.create_connection((ip, port), timeout, source_address)
        except OSError as e:
            error = e
    raise error


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = _connect_pinned  # Host header and TLS server_hostname keep the original name


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = _connect_pinned


class _PinnedHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_PinnedHTTPConnection, req)


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_PinnedHTTPSConnection, req, context=self._context)


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
        with urllib.request.build_opener(_PinnedHTTPHandler, _PinnedHTTPSHandler, _CheckedRedirect).open(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if ctype not in TYPES:
                raise TandoorError(f"the image URL sent '{ctype or 'no content type'}', not a jpeg, png, webp or gif image")
            data = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as e:
        raise TandoorError(f"image download failed ({e.code})") from None
    except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
        raise TandoorError(f"image download failed: {getattr(e, 'reason', e)}") from None
    if len(data) > MAX_BYTES:
        raise TandoorError(f"the image is larger than {MAX_BYTES // (1024 * 1024)} MB")
    return data, ctype

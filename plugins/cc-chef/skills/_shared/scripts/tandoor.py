#!/usr/bin/env python3
"""cc-chef Tandoor CLI (standard library only). Exit codes: 0 ok, 1 error, 3 not configured.

Usage: python3 tandoor.py <command> ...   (see tandoor-api.md)
"""
from __future__ import annotations

import argparse
import sys
from urllib.parse import urlsplit

import tandoor_client as tc


def _cmd_check(args: argparse.Namespace) -> int:
    cfg = tc.load_config()
    host = urlsplit(cfg.url)
    if host.scheme == "http" and host.hostname not in ("localhost", "127.0.0.1"):
        print("Warning: TANDOOR_URL uses plain http://, so the token travels unencrypted", file=sys.stderr)
    client = tc.Client(cfg)
    version = str(client.get("api/server-settings/current/").get("version", "?"))
    client.get("api/food/", {"page_size": 1})  # proves the token
    if version.split(".")[0].isdigit() and int(version.split(".")[0]) < 2:
        print(f"Warning: Tandoor {version} is older than 2.x; this plugin is built against 2.x", file=sys.stderr)
    print(f"OK: {cfg.url}, Tandoor {version}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc-chef Tandoor tool")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check", help="verify TANDOOR_URL and TANDOOR_TOKEN")
    p.set_defaults(func=_cmd_check)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except tc.NotConfigured as e:
        print(str(e), file=sys.stderr)
        return 3
    except tc.TandoorError as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

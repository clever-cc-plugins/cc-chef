"""Opt-in check of the Tandoor support against a real instance (plan Task 11).

Not a unittest: the file name keeps it out of `discover`.

    python3 tests/tandoor/live_smoke.py --run [--report FILE]

Needs TANDOOR_URL and TANDOOR_TOKEN (write scope) in the environment. It drives the real
`tandoor.py` CLI (match, preview, upload, pull), creates one recipe `cc-chef-test-<date>` and a few
foods, and deletes them again in `finally`. Use a test instance.
"""

import argparse
import base64
import datetime
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
TOOL = SCRIPTS / "tandoor.py"
sys.path.insert(0, str(SCRIPTS))

import tandoor_client as tc  # noqa: E402

DATE = datetime.date.today().isoformat()
TITLE = f"cc-chef-test-{DATE}"
FOOD_A, FOOD_B = "Cctestmehl", "Cctestzwiebel"  # A is seeded with details and properties, B is created by the upload
PROPERTY_TYPE = "cctest-kcal"
KEYWORDS = ("cctest", "cc-chef")
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")

RECIPE = f"""---
cc-chef: 1
title: {TITLE}
language: de
servings: 2
tags: [cctest]
---

# {TITLE}

Smoke test.

## Zubereitung

### 1. Ansetzen

- **200 g** {FOOD_A}
- **2** {FOOD_B}, gehackt

Alles mischen.

### 2. Garen

- **1** {FOOD_B}

Zehn Minuten garen.
"""

results: list[tuple[str, str, str]] = []
client = tc.Client(tc.load_config())


def api(method, path, body=None, params=None):
    return client._request(method, path, params, body)


def record(status, name, detail=""):
    results.append((status, name, detail))
    print(f"{status:5} {name}" + (f": {detail}" if detail else ""), flush=True)


def check(name, ok, detail=""):
    record("PASS" if ok else "FAIL", name, "" if ok else detail)


def info(name, detail):
    record("INFO", name, detail)


def cli(*args):
    return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True)


def diff(before: dict, after: dict) -> list[str]:
    return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))


def status_of(path):
    try:
        api("GET", path)
        return 200
    except tc.TandoorError as e:
        return e.status


def find(path, name, key="name", **params):
    return [r for r in client.list_all(path, params) if r.get(key) == name]


def put_image(recipe_id):
    boundary = "----cctest"
    head = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="t.png"\r\nContent-Type: image/png\r\n\r\n'
    body = head.encode() + PNG + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{client.config.url}/api/recipe/{recipe_id}/image/", data=body, method="PUT")
    req.add_header("Authorization", f"Bearer {client.config.token}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    urllib.request.urlopen(req, timeout=30).read()


def cleanup(keep_kw: set, keep_units: set):
    """Delete everything this script creates, by exact name. Returns (kind, id) pairs to confirm as gone."""
    gone = []
    for r in client.list_all("api/recipe/", {"query": TITLE}):
        if r["name"] == TITLE:
            steps = [s["id"] for s in api("GET", f"api/recipe/{r['id']}/")["steps"]]
            api("DELETE", f"api/recipe/{r['id']}/")
            gone.append(("recipe", r["id"]))
            for sid in steps:
                if status_of(f"api/step/{sid}/") == 200:
                    info("orphan step after recipe delete", f"step {sid} still exists; removing it")
                    api("DELETE", f"api/step/{sid}/")
    for name in (FOOD_A, FOOD_B):
        for r in find("api/food/", name, query=name):
            api("DELETE", f"api/food/{r['id']}/")
            gone.append(("food", r["id"]))
    for r in client.list_all("api/keyword/"):
        if r["name"] in KEYWORDS and r["name"] not in keep_kw:
            api("DELETE", f"api/keyword/{r['id']}/")
            gone.append(("keyword", r["id"]))
    for r in client.list_all("api/unit/"):
        if r["name"] == "g" and "g" not in keep_units:
            api("DELETE", f"api/unit/{r['id']}/")
            gone.append(("unit", r["id"]))
    for r in client.list_all("api/property-type/"):
        if r["name"] == PROPERTY_TYPE:
            rows = [p for p in client.list_all("api/property/") if p["property_type"]["id"] == r["id"]]
            if rows:
                info("property rows left after the food delete", f"{len(rows)} for type {r['id']}; removing them")
            for p in rows:
                api("DELETE", f"api/property/{p['id']}/")
            api("DELETE", f"api/property-type/{r['id']}/")
            gone.append(("property-type", r["id"]))
    return gone


def run_update(tmp, rid):
    backup = tmp / "backup.json"
    pulled = cli("pull", rid, "-o", backup)
    lines = dict(line.split(": ", 1) for line in pulled.stdout.splitlines() if line.startswith("tandoor-"))
    check("pull prints the recipe and its tandoor-id", pulled.returncode == 0 and "Alles mischen." in pulled.stdout and lines.get("tandoor-id") == str(rid), pulled.stderr[:300])
    if pulled.returncode != 0 or "tandoor-updated-at" not in lines:
        return False
    # the pulled text is a template to rework: carry the ids into the front matter of a changed recipe
    ids = f"tandoor-id: {rid}\ntandoor-updated-at: {lines['tandoor-updated-at']}\n"
    md = tmp / "update.md"
    md.write_text(RECIPE.replace("tags: [cctest]\n", "tags: [cctest]\n" + ids).replace("Alles mischen.", "Alles gut mischen."), encoding="utf-8")
    plan = tmp / "update-plan.json"
    m = cli("match", md, "-o", plan)
    if m.returncode != 0 or any(line.startswith("OPEN") for line in m.stdout.splitlines()):
        check("update: match", False, (m.stdout + m.stderr)[:400])
        return False
    prev = cli("preview", plan)
    if prev.returncode != 0 or "Confirm: " not in prev.stdout:
        check("update: preview", False, (prev.stdout + prev.stderr)[:400])
        return False
    up = cli("upload", plan, "--confirm", prev.stdout.split("Confirm: ")[1].split()[0])
    check("update: upload", up.returncode == 0, (up.stdout + up.stderr)[:400])
    return up.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="confirm that this writes to the instance in TANDOOR_URL")
    ap.add_argument("--report")
    args = ap.parse_args()
    if not args.run:
        print(__doc__)
        return 2
    version = api("GET", "api/server-settings/current/").get("version")
    print(f"instance {client.config.url}, Tandoor {version}\n")
    keep_kw = {r["name"] for r in client.list_all("api/keyword/")} & set(KEYWORDS)
    keep_units = {r["name"] for r in client.list_all("api/unit/")} & {"g"}
    left = cleanup(keep_kw, keep_units)
    if left:
        info("removed leftovers of an earlier run", str(left))
    if "g" not in keep_units:
        api("POST", "api/unit/", {"name": "g"})
    tmp = Path(tempfile.mkdtemp())
    rid = None
    old_steps: list[int] = []
    try:
        # seed food A with values that differ from the defaults, so "unchanged" means something
        pt = api("POST", "api/property-type/", {"name": PROPERTY_TYPE, "unit": "kcal"})
        a = api("POST", "api/food/", {"name": FOOD_A, "plural_name": "Cctestmehle", "description": "seed description"})
        api("PATCH", f"api/food/{a['id']}/", {"properties": [{"property_type": {"id": pt["id"], "name": PROPERTY_TYPE}, "property_amount": 364}]})
        before = api("GET", f"api/food/{a['id']}/")
        seeded = bool(before["plural_name"] and before["description"] and before["properties"])
        check("setup: food has plural_name, description and properties", seeded, json.dumps({k: before.get(k) for k in ("plural_name", "description", "properties")}))
        if not seeded:
            return 1

        # upload through the real CLI: match, preview, upload
        md, plan = tmp / "recipe.md", tmp / "plan.json"
        md.write_text(RECIPE, encoding="utf-8")
        m = cli("match", md, "-o", plan)
        check("create: match", m.returncode == 0, m.stderr[:300])
        plan_json = json.loads(plan.read_text(encoding="utf-8"))
        info("plan: foods", json.dumps({k: (v["status"], v["decision"], v["id"]) for k, v in plan_json["foods"].items()}))
        for kind in ("food", "unit", "keyword"):
            for key, e in plan_json[kind + "s"].items():
                if e["decision"] is None:
                    cli("resolve", plan, "--kind", kind, "--text", e["text"], "--create")
        prev = cli("preview", plan)
        check("create: preview", prev.returncode == 0 and "Confirm: " in prev.stdout, (prev.stdout + prev.stderr)[:400])
        up = cli("upload", plan, "--confirm", prev.stdout.split("Confirm: ")[1].split()[0])
        check("create: upload", up.returncode == 0, (up.stdout + up.stderr)[:400])

        found = api("GET", "api/recipe/", {"query": TITLE})["results"]
        check("assumption: GET /api/recipe/?query=<title> finds the recipe", len([r for r in found if r["name"] == TITLE]) == 1, f"{len(found)} hits")
        rid = found[0]["id"]

        after = api("GET", f"api/food/{a['id']}/")
        check("RISK: upload with {id, name} leaves the food unchanged", not diff(before, after), f"changed keys: {diff(before, after)}")
        check("upload created the second food once", len(find("api/food/", FOOD_B, query=FOOD_B)) == 1)

        # values that the update must keep
        put_image(rid)
        api("POST", "api/cook-log/", {"recipe": rid, "rating": 5})
        api("PATCH", f"api/recipe/{rid}/", {"private": True})
        r1 = api("GET", f"api/recipe/{rid}/")
        set_up = bool(r1.get("image")) and r1.get("rating") == 5 and r1.get("private") is True
        check("setup: image, rating and private are set", set_up, f"image={bool(r1.get('image'))} rating={r1.get('rating')} private={r1.get('private')}")
        old_steps = [s["id"] for s in r1["steps"]]
        old_ingredients = [i["id"] for s in r1["steps"] for i in s["ingredients"]]

        # note-only PATCH on one ingredient
        ing = r1["steps"][0]["ingredients"][0]
        api("PATCH", f"api/ingredient/{ing['id']}/", {"note": "cctest-note"})
        got = api("GET", f"api/ingredient/{ing['id']}/")
        check("note-only PATCH changes only the note", diff(ing, got) == ["note"] and got["note"] == "cctest-note", f"changed keys: {diff(ing, got)}")

        # 4.4 assumptions
        rows = client.list_all("api/ingredient/", {"food": a["id"]})
        used = rows[0].get("used_in_recipes") if rows else None
        info("used_in_recipes on GET /api/ingredient/", json.dumps(used))
        check("assumption: used_in_recipes holds {id, name}", bool(used) and all(isinstance(u, dict) and {"id", "name"} <= set(u) for u in used), json.dumps(used))
        plain, ext = api("GET", f"api/food/{a['id']}/"), api("GET", f"api/food/{a['id']}/", params={"extended": 1})
        info("food single entry numrecipe", f"without extended: {plain.get('numrecipe', '<absent>')}; with extended=1: {ext.get('numrecipe', '<absent>')}")
        check("assumption: single GET ?extended=1 returns numrecipe", ext.get("numrecipe") == 1, f"got {ext.get('numrecipe', '<absent>')}")
        for path in ("api/food/", "api/unit/"):
            for value in (None, 1, "true"):
                params = {"page_size": 200, **({} if value is None else {"extended": value})}
                rows = api("GET", path, params)["results"]
                info(f"{path} list, extended={value}", json.dumps([{"name": x["name"], "numrecipe": x.get("numrecipe", "<absent>")} for x in rows]))

        # update through the real CLI: pull, edit, match, preview, upload
        if run_update(tmp, rid):
            r2 = api("GET", f"api/recipe/{rid}/")
            check("update replaced the steps", "Alles gut mischen." in json.dumps(r2["steps"]))
            check("update keeps image, rating and private", bool(r2.get("image")) and r2.get("rating") == 5 and r2.get("private") is True,
                  f"image={bool(r2.get('image'))} rating={r2.get('rating')} private={r2.get('private')}")
            changed = diff(before, api("GET", f"api/food/{a['id']}/"))
            check("update leaves the food unchanged", not changed, f"changed keys: {changed}")
            orphans = [sid for sid in old_steps if status_of(f"api/step/{sid}/") == 200 and sid not in [s["id"] for s in r2["steps"]]]
            info("replaced steps left behind as orphans", f"{len(orphans)} of {len(old_steps)}: {orphans}")
            orphan_ing = [i for i in old_ingredients if status_of(f"api/ingredient/{i}/") == 200 and i not in [x["id"] for s in r2["steps"] for x in s["ingredients"]]]
            info("replaced ingredients left behind as orphans", f"{len(orphan_ing)} of {len(old_ingredients)}")
        return 0
    finally:
        gone = cleanup(keep_kw, keep_units)
        for kind, i in gone:
            path = {"property-type": "api/property-type", "keyword": "api/keyword"}.get(kind, f"api/{kind}")
            check(f"cleanup: {kind} {i} is gone", status_of(f"{path}/{i}/") == 404)
        if args.report:
            Path(args.report).write_text(json.dumps({"version": version, "date": DATE, "results": results}, indent=2), encoding="utf-8")
        failed = [r for r in results if r[0] == "FAIL"]
        print(f"\n{len(results)} results, {len(failed)} FAIL")


if __name__ == "__main__":
    code = main()
    sys.exit(code or (1 if any(r[0] == "FAIL" for r in results) else 0))

#!/usr/bin/env python3
"""Fail if a reference file copies 12 or more consecutive words from any research report.

Usage: check_overlap.py <ref-file> '<research-glob>'   (quote the glob)

Words are case-folded and stripped of punctuation. Exit 1 prints every copied
passage and the report it came from; exit 0 means no overlap; exit 2 is a usage error.
"""
import glob
import os
import re
import sys

N = 12


def words(path):
    with open(path, encoding="utf-8") as f:
        return re.sub(r"[\W_]+", " ", f.read().casefold()).split()


def main(argv):
    if len(argv) != 3:
        print("usage: check_overlap.py <ref-file> '<research-glob>'", file=sys.stderr)
        return 2
    ref_path, pattern = argv[1], argv[2]
    reports = sorted(glob.glob(pattern))
    if not reports:
        print("no research files match: " + pattern, file=sys.stderr)
        return 2
    ref = words(ref_path)
    found = False
    for report in reports:
        grams = set()
        text = words(report)
        for i in range(len(text) - N + 1):
            grams.add(tuple(text[i : i + N]))
        i = 0
        while i <= len(ref) - N:
            if tuple(ref[i : i + N]) in grams:
                j = i + N
                while j < len(ref) and tuple(ref[j - N + 1 : j + 1]) in grams:
                    j += 1
                print("copied from %s: \"%s\"" % (os.path.basename(report), " ".join(ref[i:j])))
                found = True
                i = j
            else:
                i += 1
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
